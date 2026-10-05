from mcp_server import MCPToolset
from typing import Any

from .models import Post

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
                    "content": post.content,
            }
        
        return result

    def create_post(self):
        ...
        
    def update_post(self):
        ...
    