from mcp_server import MCPToolset
from django.core.exceptions import ValidationError
from django.db import transaction

from typing import Any
import hashlib

from .models import Post, Category, Tag
from .schemas import (
    PostCreateInput,
    PostChangesInput,
    ContentPatchInput,
    )


def _calculate_content_revision(content: str) -> str:
    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()

class PostTools(MCPToolset):
    
    def list_all_posts(self) -> list[dict[str, Any]]:
        posts = (
            Post
            .objects
            .select_related("category", "created_by")
            .prefetch_related("tags")
            .order_by('-created_at')
            )
        
        results = [
            {
                "id": post.id,
                "title": post.title,
                "excerpt": post.excerpt,
                "category": post.category.name if post.category else None,
                "created_by": post.created_by.first_name if post.created_by else None,
                "tags": [
                    {
                    "name": tag.name,
                    "id": tag.id
                    }
                    for tag in post.tags.all()
                ],
                "created_at": post.created_at.isoformat(),
                "updated_at": post.updated_at.isoformat(),
            }
            for post in posts
        ]
        
        return results
    
    def show_post_detail(self, id:int):
        post = (
            Post
            .objects
            .filter(pk=id)
            .first()
        )
        
        if post is None:
            raise ValueError(f"Post id={id} não encontrado.")
        
        cover_url = post.cover.url if post.cover else None
        if cover_url and getattr(self, 'request', None) is not None:
            cover_url = self.request.build_absolute_uri(cover_url)
           
        content = post.content or ""
         
        result = {
                    "id": post.id,
                    "title": post.title,
                    "slug": post.slug,                    
                    "excerpt": post.excerpt,
                    "category": post.category.name if post.category else None,
                    "created_by": post.created_by.first_name if post.created_by else None,
                    "is_published": post.is_published,
                    "tags": [
                        {
                        "name": tag.name,
                        "id": tag.id
                        }
                        for tag in post.tags.all()
                    ],
                    "created_at": post.created_at.isoformat(),
                    "updated_at": post.updated_at.isoformat(),
                    "cover": cover_url,
                    "cover_caption": post.cover_caption, 
                    "content": content,
                    "content_revision_hash": _calculate_content_revision(content),
            }
        
        return result

    @transaction.atomic
    def create_post(
        self,
        post_data: PostCreateInput,
    ) -> dict[str, Any]:
        clean_title = post_data.title.strip()
        clean_excerpt = post_data.excerpt.strip()
        clean_slug = post_data.slug.strip() if post_data.slug else ""
        
        if not clean_title:
            raise ValueError("title não pode ficar vazio.")
        
        if len(clean_title) > 125:
            raise ValueError("Titulo deve ter no máximo 125 caractéres.")
        
        if not clean_excerpt:
            raise ValueError("excerpt não pode ficar vazio.")
        
        if len(clean_excerpt) > 160:
            raise ValueError("Excerpet deve ter no máximo 160 caracteres.")
        
        if not post_data.content.strip():
            raise ValueError("content não pode ficar vazio.")
        
        category = None
        if post_data.category_id is not None:
            category = (
                Category.objects
                .filter(pk=post_data.category_id)
                .first()
            )
            
            if category is None:
                raise ValueError(
                    f"Categoria id={post_data.category_id} não encontrada"
                )
        
        tags = []
        if post_data.tag_ids is not None:
            unique_tag_ids = list(dict.fromkeys(post_data.tag_ids))
            tags = list(Tag.objects.filter(pk__in=unique_tag_ids))
            
            found_tags_ids = {tag.id for tag in tags}
            missing_tag_ids = set(unique_tag_ids) - found_tags_ids
            if missing_tag_ids:
                missing = ", ".join(str(tag_id) for tag_id in sorted(missing_tag_ids))
                raise ValueError(f"Tags não encontradas: {missing}")
            
        post = Post(
            title=clean_title,
            excerpt=clean_excerpt,
            slug=clean_slug,
            content=post_data.content,
            category=category,
            is_published=False,
        )
        
        try:
            post.full_clean()
        except ValidationError as error:
            raise ValueError("; ".join(error.messages)) from error
        
        post.save()
        
        if tags:
            post.tags.set(tags)
            
        return {
            "post_id": post.id,
            "title": post.title,
            "slug": post.slug,
            "category_id": post.category_id,
            "tag_ids": list(
                post.tags.values_list("id", flat=True)
                
            ),
            "is_published": post.is_published,
            "message":f"Post {post.id} criado como rascunho",
        }
         
    @transaction.atomic   
    def update_post(
        self,
        post_id: int,
        changes: PostChangesInput | None = None,
        content_revision_hash: str | None = None,
        content_patches: list[ContentPatchInput] | None = None,
        ) -> dict[str, Any]:
        
        post = (
            Post.objects
            .select_for_update()
            .filter(pk=post_id)
            .first()
            )
        
        if post is None:
            raise ValueError(f"Post id={post_id} não encontrado")
        
        changes_data = (
            changes.model_dump(exclude_unset=True)
            if changes is not None
            else {}
        )
        
        if not changes_data and not content_patches:
            raise ValueError("Informe ao menos uma alteração.")
        
        updated_fields: list[str] = []
        if content_patches:
            if not content_revision_hash:
                raise ValueError(
                    "content_revision_hash é obrigatório "
                    "para atualizar o conteúdo."
                )
                
            current_content = post.content or ""
            
            current_revision_hash = _calculate_content_revision(current_content)
        
            if content_revision_hash != current_revision_hash:
                raise ValueError(
                    "O conteúdo foi alterado desde a última leitura. "
                    "Leia o post novamente antes de atualizar."
                )
        
            patched_content = current_content
            for index, patch in enumerate(content_patches):
                target_html = patch.target_html
                replacement_html = patch.replacement_html  

                occurrences = patched_content.count(target_html)
                if occurrences == 0:
                    raise ValueError(
                        f"Patch {index}: o trecho não foi encontrado."
                    )
                    
                if occurrences > 1:
                    raise ValueError(
                        f"Patch {index}: o trecho aparece "
                        f"{occurrences} vezes. Inclua mais HTML ao redor."
                    )
                
                patched_content = patched_content.replace(
                    target_html,
                    replacement_html,
                    1
                )
                
            post.content = patched_content
            updated_fields.append("content")

        category_id_provided = "category_id" in changes_data
        category_id = changes_data.pop("category_id", None)

        tag_ids_provided = "tag_ids" in changes_data
        tag_ids = changes_data.pop("tag_ids", None)

        if category_id_provided:
            category = None

            if category_id is not None:
                category = (
                    Category
                    .objects
                    .filter(pk=category_id)
                    .first()
                    )

                if category is None:
                    raise ValueError(
                        f"Categoria id={category_id} não encontrada."
                    )

            post.category = category
            updated_fields.append("category")

        # Update tags
        tags_to_set: list[Tag] = []
        if tag_ids_provided:
            if not isinstance(tag_ids, list):
                raise ValueError(
                    "tag_ids deve ser uma lista de números inteiros."
                )

            invalid_tag_ids = [
                tag_id
                for tag_id in tag_ids
                if not isinstance(tag_id, int)
                or isinstance(tag_id, bool)
            ]

            if invalid_tag_ids:
                raise ValueError(
                    "Todos os valores de tag_ids devem ser inteiros."
                )

            unique_tag_ids = list(dict.fromkeys(tag_ids))
            tags_to_set = list(
                Tag.objects.filter(pk__in=unique_tag_ids)
            )

            found_tag_ids = {
                tag.id
                for tag in tags_to_set
            }

            missing_tag_ids = set(unique_tag_ids) - found_tag_ids

            if missing_tag_ids:
                missing = ", ".join(
                    str(tag_id)
                    for tag_id in sorted(missing_tag_ids)
                )
                raise ValueError(
                    f"Tags não encontradas: {missing}"
                )

        for field, value in changes_data.items():
            if field in {"title", "excerpt"}:
                if not isinstance(value, str):
                    raise ValueError(
                        f"{field} deve ser uma string."
                    )
                
                value = value.strip()
                
                if not value:
                    raise ValueError(
                        f"{field} não pode ficar vazio"
                    )
                    
            elif field == "slug":
                if value is None:
                    value = ""
                
                elif not isinstance(value, str):
                    raise ValueError(
                        "slug deve ser uma string."
                    )
                else:
                    value = value.strip()
                    
            setattr(post, field, value)
            updated_fields.append(field)
        
        try:
            post.full_clean()
        except ValidationError as error:
            raise ValueError(
                "; ".join(error.messages)
            ) from error
            
        fields_to_save = list(
            dict.fromkeys([
                *updated_fields,
                "updated_at",
            ])
        )
        
        post.save(update_fields=fields_to_save)
            
        if tag_ids_provided:
            post.tags.set(tags_to_set)
        
        response_updated_fields = [
            "category_id" if field == "category" else field
            for field in updated_fields
        ]
        
        if tag_ids_provided:
            response_updated_fields.append("tag_ids")
        
        response_updated_fields = list(
            dict.fromkeys(response_updated_fields)
        )
        return {
            "post_id":post.id,
            "updated_fields": response_updated_fields,
            "category_id": post.category_id,
            "tag_ids": list(
                post.tags.values_list('id', flat=True)
            ),
            "content_revision_hash": (
                _calculate_content_revision(post.content or "") 
            ),
            "updated_at": post.updated_at.isoformat(),
            "message": f"Post {post.id} atualizado com sucesso",
        }
