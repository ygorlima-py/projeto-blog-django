import hashlib

from django.test import SimpleTestCase, TestCase
from pydantic import ValidationError

from blog.mcp import PostTools
from blog.models import Category, Post, Tag
from blog.schemas import ContentPatchInput, PostChangesInput, PostCreateInput


class PostMCPInputSchemaTests(SimpleTestCase):
    def test_create_input_rejects_blank_html_and_unknown_fields(self):
        with self.assertRaises(ValidationError):
            PostCreateInput(
                title="Novo post",
                excerpt="Resumo do novo post.",
                content="   ",
            )

        with self.assertRaises(ValidationError):
            PostCreateInput(
                title="Novo post",
                excerpt="Resumo do novo post.",
                content="<p>Conteúdo</p>",
                is_published=True,
            )

    def test_update_input_does_not_accept_protected_fields(self):
        with self.assertRaises(ValidationError):
            PostChangesInput(is_published=True)

    def test_content_patch_requires_a_non_empty_target(self):
        with self.assertRaises(ValidationError):
            ContentPatchInput(
                target_html="",
                replacement_html="<p>Novo conteúdo</p>",
            )


class PostMCPTests(TestCase):
    def setUp(self):
        self.tools = PostTools()
        self.category = Category.objects.create(
            name="Tailândia",
            slug="tailandia",
        )
        self.other_category = Category.objects.create(
            name="Vietnã",
            slug="vietna",
        )
        self.tag_food = Tag.objects.create(name="Gastronomia", slug="gastronomia")
        self.tag_travel = Tag.objects.create(name="Viagem", slug="viagem")

    def make_post(self, **overrides):
        post_number = Post.objects.count() + 1
        data = {
            "title": f"Post existente {post_number}",
            "slug": f"post-existente-{post_number}",
            "excerpt": "Resumo de um post existente.",
            "content": "<p>Conteúdo existente.</p>",
            "category": self.category,
        }
        data.update(overrides)
        return Post.objects.create(**data)

    def make_create_input(self, **overrides):
        data = {
            "title": "Novo post sobre Chiang Mai",
            "excerpt": "Um resumo sobre Chiang Mai.",
            "content": "<p>Conteúdo inicial.</p>",
        }
        data.update(overrides)
        return PostCreateInput(**data)

    def test_list_all_posts_returns_summary_in_descending_creation_order(self):
        older_post = self.make_post(title="Post antigo", slug="post-antigo")
        newer_post = self.make_post(title="Post novo", slug="post-novo")
        newer_post.tags.add(self.tag_travel)

        result = self.tools.list_all_posts()

        self.assertEqual([item["id"] for item in result], [newer_post.id, older_post.id])
        self.assertEqual(result[0]["category"], self.category.name)
        self.assertEqual(
            result[0]["tags"],
            [{"id": self.tag_travel.id, "name": self.tag_travel.name}],
        )
        self.assertNotIn("content", result[0])

    def test_show_post_detail_returns_content_and_revision_hash(self):
        post = self.make_post(
            content="<p>Introdução</p><table><tr><td>Valor</td></tr></table>",
        )

        result = self.tools.show_post_detail(post.id)

        self.assertEqual(result["id"], post.id)
        self.assertEqual(result["content"], post.content)
        self.assertEqual(
            result["content_revision_hash"],
            hashlib.sha256(post.content.encode("utf-8")).hexdigest(),
        )

    def test_show_post_detail_rejects_unknown_post(self):
        with self.assertRaisesMessage(ValueError, "Post id=999999 não encontrado"):
            self.tools.show_post_detail(999999)

    def test_create_post_creates_a_draft_with_category_and_unique_tags(self):
        result = self.tools.create_post(
            self.make_create_input(
                title="  Guia de Chiang Mai  ",
                excerpt="  Onde comer e o que visitar.  ",
                category_id=self.category.id,
                tag_ids=[self.tag_food.id, self.tag_food.id, self.tag_travel.id],
            ),
        )
        post = Post.objects.get(pk=result["post_id"])

        self.assertEqual(post.title, "Guia de Chiang Mai")
        self.assertEqual(post.excerpt, "Onde comer e o que visitar.")
        self.assertFalse(post.is_published)
        self.assertEqual(post.category_id, self.category.id)
        self.assertSetEqual(
            set(post.tags.values_list("id", flat=True)),
            {self.tag_food.id, self.tag_travel.id},
        )
        self.assertRegex(post.slug, r"^guia-de-chiang-mai-[a-z0-9]{3}$")

    def test_create_post_rejects_unknown_tags_without_creating_a_post(self):
        post_count_before = Post.objects.count()

        with self.assertRaisesMessage(ValueError, "Tags não encontradas: 999999"):
            self.tools.create_post(
                self.make_create_input(
                    tag_ids=[self.tag_food.id, 999999],
                ),
            )

        self.assertEqual(Post.objects.count(), post_count_before)

    def test_update_post_updates_regular_fields_and_preserves_omitted_values(self):
        post = self.make_post(category=self.category)
        post.tags.add(self.tag_food, self.tag_travel)

        result = self.tools.update_post(
            post_id=post.id,
            changes=PostChangesInput(
                title="  Título atualizado  ",
                slug=None,
                category_id=None,
                tag_ids=[],
            ),
        )
        post.refresh_from_db()

        self.assertEqual(post.title, "Título atualizado")
        self.assertEqual(post.excerpt, "Resumo de um post existente.")
        self.assertRegex(post.slug, r"^titulo-atualizado-[a-z0-9]{3}$")
        self.assertIsNone(post.category_id)
        self.assertFalse(post.tags.exists())
        self.assertSetEqual(
            set(result["updated_fields"]),
            {"title", "slug", "category_id", "tag_ids"},
        )

    def test_update_post_replaces_category_and_tags(self):
        post = self.make_post(category=self.category)
        post.tags.add(self.tag_food)

        result = self.tools.update_post(
            post_id=post.id,
            changes=PostChangesInput(
                category_id=self.other_category.id,
                tag_ids=[self.tag_travel.id, self.tag_travel.id],
            ),
        )
        post.refresh_from_db()

        self.assertEqual(post.category_id, self.other_category.id)
        self.assertEqual(
            list(post.tags.values_list("id", flat=True)),
            [self.tag_travel.id],
        )
        self.assertSetEqual(
            set(result["updated_fields"]),
            {"category_id", "tag_ids"},
        )

    def test_update_post_rejects_unknown_tags_without_changing_existing_tags(self):
        post = self.make_post()
        post.tags.add(self.tag_food)

        with self.assertRaisesMessage(ValueError, "Tags não encontradas: 999999"):
            self.tools.update_post(
                post_id=post.id,
                changes=PostChangesInput(tag_ids=[999999]),
            )

        self.assertEqual(
            list(post.tags.values_list("id", flat=True)),
            [self.tag_food.id],
        )

    def test_update_post_replaces_only_the_requested_html_fragment(self):
        post = self.make_post(
            content=(
                "<p>Introdução preservada.</p>"
                "<table><tbody><tr><td>Preço antigo</td></tr></tbody></table>"
                "<p>Conclusão preservada.</p>"
            ),
        )
        detail = self.tools.show_post_detail(post.id)

        result = self.tools.update_post(
            post_id=post.id,
            content_revision_hash=detail["content_revision_hash"],
            content_patches=[
                ContentPatchInput(
                    target_html="<td>Preço antigo</td>",
                    replacement_html="<td>Preço atualizado</td>",
                ),
            ],
        )
        post.refresh_from_db()

        self.assertIn("<p>Introdução preservada.</p>", post.content)
        self.assertIn("<td>Preço atualizado</td>", post.content)
        self.assertIn("<p>Conclusão preservada.</p>", post.content)
        self.assertNotIn("Preço antigo", post.content)
        self.assertEqual(result["updated_fields"], ["content"])
        self.assertEqual(
            result["content_revision_hash"],
            self.tools.show_post_detail(post.id)["content_revision_hash"],
        )

    def test_update_post_applies_content_patches_in_sequence(self):
        post = self.make_post(content="<p>Rascunho</p>")
        detail = self.tools.show_post_detail(post.id)

        self.tools.update_post(
            post_id=post.id,
            content_revision_hash=detail["content_revision_hash"],
            content_patches=[
                ContentPatchInput(
                    target_html="<p>Rascunho</p>",
                    replacement_html="<p>Revisão</p>",
                ),
                ContentPatchInput(
                    target_html="<p>Revisão</p>",
                    replacement_html="<p>Versão final</p>",
                ),
            ],
        )
        post.refresh_from_db()

        self.assertEqual(post.content, "<p>Versão final</p>")

    def test_update_post_requires_hash_when_content_patches_are_sent(self):
        post = self.make_post(content="<p>Conteúdo original</p>")

        with self.assertRaisesMessage(
            ValueError,
            "content_revision_hash é obrigatório",
        ):
            self.tools.update_post(
                post_id=post.id,
                content_patches=[
                    ContentPatchInput(
                        target_html="<p>Conteúdo original</p>",
                        replacement_html="<p>Conteúdo alterado</p>",
                    ),
                ],
            )

        post.refresh_from_db()
        self.assertEqual(post.content, "<p>Conteúdo original</p>")

    def test_update_post_rejects_a_stale_content_hash_without_changing_content(self):
        post = self.make_post(content="<p>Versão original</p>")
        stale_hash = self.tools.show_post_detail(post.id)["content_revision_hash"]
        post.content = "<p>Versão mais recente</p>"
        post.save()

        with self.assertRaisesMessage(
            ValueError,
            "O conteúdo foi alterado desde a última leitura",
        ):
            self.tools.update_post(
                post_id=post.id,
                content_revision_hash=stale_hash,
                content_patches=[
                    ContentPatchInput(
                        target_html="<p>Versão original</p>",
                        replacement_html="<p>Tentativa desatualizada</p>",
                    ),
                ],
            )

        post.refresh_from_db()
        self.assertEqual(post.content, "<p>Versão mais recente</p>")

    def test_update_post_rolls_back_regular_changes_when_a_patch_is_ambiguous(self):
        post = self.make_post(
            title="Título original",
            content="<p>Trecho repetido</p><p>Trecho repetido</p>",
        )
        detail = self.tools.show_post_detail(post.id)

        with self.assertRaisesMessage(
            ValueError,
            "Patch 0: o trecho aparece 2 vezes",
        ):
            self.tools.update_post(
                post_id=post.id,
                changes=PostChangesInput(title="Título que não deve salvar"),
                content_revision_hash=detail["content_revision_hash"],
                content_patches=[
                    ContentPatchInput(
                        target_html="<p>Trecho repetido</p>",
                        replacement_html="<p>Trecho novo</p>",
                    ),
                ],
            )

        post.refresh_from_db()
        self.assertEqual(post.title, "Título original")
        self.assertEqual(
            post.content,
            "<p>Trecho repetido</p><p>Trecho repetido</p>",
        )

    def test_update_post_requires_an_change_or_content_patch(self):
        post = self.make_post()

        with self.assertRaisesMessage(
            ValueError,
            "Informe ao menos uma alteração.",
        ):
            self.tools.update_post(post_id=post.id)
