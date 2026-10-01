import base64
import tempfile
from decimal import Decimal
from io import BytesIO

from django.core.exceptions import ValidationError
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from PIL import Image

from affiliates.models import AffiliateCategory, AffiliatePartner
from blog.models import Post
from site_setup.models import SiteSetup

from .mcp import StoryTools
from .models import Story, StoryElement, StorySlide
from .sitemaps import StorySitemap


class StoryTestCase(TestCase):
    def create_story(self, **overrides):
        sequence = Story.objects.count() + 1
        data = {
            "title": f"Story de teste {sequence}",
            "slug": f"story-de-teste-{sequence}",
            "cover": f"stories/cover/story-{sequence}.jpg",
            "is_published": True,
            "order": sequence,
        }
        data.update(overrides)
        return Story.objects.create(**data)

    def create_slide(self, story, **overrides):
        sequence = story.slides.count() + 1
        data = {
            "story": story,
            "image": f"stories/slides/slide-{story.pk}-{sequence}.jpg",
            "alt_text": f"Imagem do slide {sequence}",
            "order": sequence,
        }
        data.update(overrides)
        return StorySlide.objects.create(**data)

    def create_partner(self, **overrides):
        sequence = AffiliatePartner.objects.count() + 1
        category = AffiliateCategory.objects.create(
            name=f"Categoria {sequence}",
            slug=f"categoria-{sequence}",
        )
        data = {
            "category": category,
            "name": f"Parceiro {sequence}",
            "description": "Descrição do parceiro de teste.",
            "image": f"affiliates/partner-{sequence}.jpg",
            "cta_icon": f"affiliates/cta-icons/partner-{sequence}.webp",
            "image_alt": "Imagem do parceiro",
            "affiliate_url": "https://parceiro.example/oferta",
            "button_label": "Conhecer parceiro",
            "is_published": True,
        }
        data.update(overrides)
        return AffiliatePartner.objects.create(**data)

    def create_post(self, **overrides):
        sequence = Post.objects.count() + 1
        data = {
            "title": f"Post relacionado {sequence}",
            "slug": f"post-relacionado-{sequence}",
            "excerpt": "Resumo do post relacionado.",
            "content": "Conteúdo do post relacionado.",
            "cover": f"posts/post-{sequence}.jpg",
            "is_published": True,
        }
        data.update(overrides)
        return Post.objects.create(**data)


class StoryModelTests(StoryTestCase):
    def test_story_generates_slug_when_missing(self):
        story = Story.objects.create(
            title="Koh Larn: praias e natureza",
            cover="stories/cover/koh-larn.jpg",
        )

        self.assertEqual(story.slug, "koh-larn-praias-e-natureza")

    def test_story_absolute_url_uses_detail_route(self):
        story = self.create_story(slug="koh-larn")

        self.assertEqual(
            story.get_absolute_url(),
            reverse("stories:detail", kwargs={"slug": "koh-larn"}),
        )

    def test_published_and_unpublished_stories_are_stored(self):
        published = self.create_story(slug="publicada", is_published=True)
        draft = self.create_story(slug="rascunho", is_published=False)

        self.assertTrue(Story.objects.get(pk=published.pk).is_published)
        self.assertFalse(Story.objects.get(pk=draft.pk).is_published)


class StoryElementValidationTests(StoryTestCase):
    def setUp(self):
        super().setUp()
        self.story = self.create_story()
        self.slide = self.create_slide(self.story)
        self.partner = self.create_partner()
        self.post = self.create_post()

    def test_cta_without_destination_is_invalid(self):
        element = StoryElement(
            slide=self.slide,
            element_type=StoryElement.ElementType.CTA,
            text="Abrir destino",
        )

        with self.assertRaisesMessage(
            ValidationError,
            "Escolha um parceiro afiliado ou um post.",
        ):
            element.full_clean()

    def test_cta_with_affiliate_and_post_is_invalid(self):
        element = StoryElement(
            slide=self.slide,
            element_type=StoryElement.ElementType.CTA,
            text="Abrir destino",
            affiliate_partner=self.partner,
            post=self.post,
        )

        with self.assertRaisesMessage(
            ValidationError,
            "Escolha somente um destino: afiliado ou post.",
        ):
            element.full_clean()

    def test_cta_with_only_affiliate_is_valid(self):
        element = StoryElement(
            slide=self.slide,
            element_type=StoryElement.ElementType.CTA,
            text="Conhecer parceiro",
            affiliate_partner=self.partner,
        )

        element.full_clean()

    def test_cta_with_only_post_is_valid(self):
        element = StoryElement(
            slide=self.slide,
            element_type=StoryElement.ElementType.CTA,
            text="Ler post",
            post=self.post,
        )

        element.full_clean()

    def test_non_cta_element_requires_text(self):
        element = StoryElement(
            slide=self.slide,
            element_type=StoryElement.ElementType.TITLE,
            text="   ",
        )

        with self.assertRaisesMessage(
            ValidationError,
            "Informe o texto do elemento.",
        ):
            element.full_clean()


class StoryDetailViewTests(StoryTestCase):
    def test_published_story_returns_200_and_draft_returns_404(self):
        published = self.create_story(slug="story-publicada")
        draft = self.create_story(slug="story-rascunho", is_published=False)
        self.create_slide(published)

        published_response = self.client.get(published.get_absolute_url())
        draft_response = self.client.get(draft.get_absolute_url())

        self.assertEqual(published_response.status_code, 200)
        self.assertTemplateUsed(
            published_response,
            "stories/story_detail.html",
        )
        self.assertEqual(draft_response.status_code, 404)

    def test_slides_elements_and_visual_attributes_keep_their_order(self):
        story = self.create_story(slug="story-ordenada")
        first_slide = self.create_slide(
            story,
            order=1,
            image="stories/slides/first.jpg",
            alt_text="Primeira paisagem",
        )
        second_slide = self.create_slide(
            story,
            order=2,
            image="stories/slides/second.jpg",
            alt_text="Segunda paisagem",
        )
        self.create_slide(
            story,
            order=3,
            image="stories/slides/third.jpg",
            alt_text="Terceira paisagem",
        )

        StoryElement.objects.create(
            slide=first_slide,
            element_type=StoryElement.ElementType.TEXT,
            text="Primeiro elemento",
            order=1,
            animation=StoryElement.Animation.FLY_IN_LEFT,
            delay_ms=150,
            duration_ms=900,
            variant="#112233",
            background_color="#ffffff",
            font_size_rem=Decimal("1.20"),
            font_weight=StoryElement.FontWeight.BOLD,
            font_style=StoryElement.FontStyle.ITALIC,
        )
        StoryElement.objects.create(
            slide=first_slide,
            element_type=StoryElement.ElementType.TITLE,
            text="Título inicial",
            order=2,
        )
        StoryElement.objects.create(
            slide=second_slide,
            element_type=StoryElement.ElementType.TITLE,
            text="Título final",
            order=1,
        )

        response = self.client.get(story.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'alt="Primeira paisagem"')
        self.assertContains(response, 'alt="Segunda paisagem"')
        self.assertContains(response, 'alt="Story de teste 1"')
        self.assertContains(response, "<h1>Título inicial</h1>", html=True)
        self.assertContains(response, "<h2>Título final</h2>", html=True)
        self.assertContains(response, 'animate-in="fly-in-left"')
        self.assertContains(response, 'animate-in-delay="150ms"')
        self.assertContains(response, 'animate-in-duration="900ms"')
        self.assertContains(response, "--story-text-color: #112233")
        self.assertContains(response, "--story-background-color: #ffffff")
        self.assertContains(response, "--story-font-size: 1.20rem")

        first_position = response.content.decode().index("Primeiro elemento")
        title_position = response.content.decode().index("Título inicial")
        self.assertLess(first_position, title_position)

    def test_affiliate_cta_renders_secure_external_link(self):
        story = self.create_story(slug="story-afiliado")
        slide = self.create_slide(story)
        partner = self.create_partner(
            affiliate_url="https://parceiro.example/roteiro",
        )
        StoryElement.objects.create(
            slide=slide,
            element_type=StoryElement.ElementType.CTA,
            text="Conheça o parceiro",
            affiliate_partner=partner,
        )

        response = self.client.get(story.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<amp-story-page-outlink")
        self.assertContains(
            response,
            'href="https://parceiro.example/roteiro"',
        )
        self.assertContains(response, 'target="_blank"')
        self.assertContains(
            response,
            'rel="sponsored nofollow noopener noreferrer"',
        )

    def test_post_cta_renders_related_post_link(self):
        story = self.create_story(slug="story-post")
        slide = self.create_slide(story)
        post = self.create_post(
            title="Como viajar para Koh Larn",
            slug="como-viajar-koh-larn",
        )
        StoryElement.objects.create(
            slide=slide,
            element_type=StoryElement.ElementType.CTA,
            text="Ler artigo",
            post=post,
        )

        response = self.client.get(story.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'href="{post.get_absolute_url()}"',
        )
        self.assertContains(response, post.title)
        self.assertContains(response, f'src="/media/{post.cover.name}"')

    def test_common_slide_bottom_text_and_post_outlink(self):
        story = self.create_story(slug="story-post-slide-comum")
        common_slide = self.create_slide(story, order=1)
        self.create_slide(story, order=2)
        post = self.create_post(
            title="Post no slide comum",
            slug="post-no-slide-comum",
        )
        StoryElement.objects.create(
            slide=common_slide,
            element_type=StoryElement.ElementType.TEXT,
            text="Texto na região inferior",
            position=StoryElement.Position.BOTTOM,
        )
        StoryElement.objects.create(
            slide=common_slide,
            element_type=StoryElement.ElementType.CTA,
            text="Ler post no slide",
            position=StoryElement.Position.BOTTOM,
            post=post,
        )

        response = self.client.get(story.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<amp-story-grid-layer template="fill" class="story-bottom-layer">',
        )
        self.assertContains(response, "Texto na região inferior")
        self.assertContains(response, "<amp-story-page-outlink")
        self.assertContains(
            response,
            f'cta-image="/media/{post.cover.name}"',
        )
        self.assertContains(
            response,
            f'href="{post.get_absolute_url()}"',
        )
        self.assertContains(response, "Ler post no slide")


class StoryListViewTests(StoryTestCase):
    def test_list_shows_only_published_stories(self):
        published = self.create_story(
            title="Story pública",
            slug="story-publica",
            is_published=True,
        )
        draft = self.create_story(
            title="Story privada",
            slug="story-privada",
            is_published=False,
        )

        response = self.client.get(reverse("stories:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, published.title)
        self.assertContains(response, f'href="{published.get_absolute_url()}"')
        self.assertContains(response, f'alt="{published.title}"')
        self.assertNotContains(response, draft.title)

    def test_list_paginates_eight_stories_per_page(self):
        for index in range(9):
            self.create_story(
                title=f"Story {index}",
                slug=f"story-{index}",
            )

        response = self.client.get(reverse("stories:list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["paginator"].per_page, 8)
        self.assertEqual(len(response.context["page_obj"].object_list), 8)
        self.assertEqual(response.context["paginator"].num_pages, 2)

    def test_empty_list_shows_empty_state(self):
        response = self.client.get(reverse("stories:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nenhum story publicado.")


class StorySitemapTests(StoryTestCase):
    def test_sitemap_contains_only_published_stories(self):
        published = self.create_story(slug="story-no-sitemap")
        draft = self.create_story(
            slug="story-rascunho-sitemap",
            is_published=False,
        )
        sitemap = StorySitemap()

        items = list(sitemap.items())

        self.assertIn(published, items)
        self.assertNotIn(draft, items)

    def test_sitemap_uses_story_url_and_lastmod(self):
        story = self.create_story(slug="story-no-sitemap")
        sitemap = StorySitemap()

        self.assertEqual(sitemap.location(story), story.get_absolute_url())
        self.assertEqual(sitemap.lastmod(story), story.updated_at)


class StoryURLTests(StoryTestCase):
    def test_story_list_and_detail_urls(self):
        story = self.create_story(slug="story-url")
        self.create_slide(story)

        list_response = self.client.get(reverse("stories:list"))
        detail_response = self.client.get(story.get_absolute_url())
        missing_response = self.client.get(
            reverse(
                "stories:detail",
                kwargs={"slug": "story-inexistente"},
            ),
        )

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(missing_response.status_code, 404)


class StoryMCPTests(StoryTestCase):
    def setUp(self):
        super().setUp()
        self.story = self.create_story(
            title="Story MCP",
            slug="story-mcp",
        )
        self.slide = self.create_slide(self.story)
        self.request = RequestFactory().get("/", HTTP_HOST="testserver")
        self.tools = StoryTools(request=self.request)

    def make_png_base64(self):
        image_stream = BytesIO()
        Image.new("RGB", (4, 4), color="#16a085").save(
            image_stream,
            format="PNG",
        )
        return base64.b64encode(image_stream.getvalue()).decode("ascii")

    def test_list_published_stories_returns_only_published_stories(self):
        draft = self.create_story(
            title="Story MCP em rascunho",
            slug="story-mcp-rascunho",
            is_published=False,
        )

        result = self.tools.list_published_stories()

        self.assertEqual(
            result,
            [
                {
                    "title": self.story.title,
                    "story_id": self.story.id,
                    "order": self.story.order,
                    "created_at": self.story.created_at.isoformat(),
                },
            ],
        )
        self.assertNotIn(draft.id, [story["story_id"] for story in result])

    def test_show_story_detail_returns_slides_elements_and_absolute_image_url(self):
        element = StoryElement.objects.create(
            slide=self.slide,
            element_type=StoryElement.ElementType.TITLE,
            text="Título do slide",
            order=1,
        )

        result = self.tools.show_story_detail_by_id(self.story.id)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["slide_id"], self.slide.id)
        self.assertEqual(
            result[0]["image_url"],
            f"http://testserver/media/{self.slide.image.name}",
        )
        self.assertEqual(result[0]["image_description"], self.slide.alt_text)
        self.assertEqual(result[0]["elements"][0]["element_id"], element.id)
        self.assertEqual(result[0]["elements"][0]["text"], "Título do slide")

    def test_create_story_element_persists_element_on_slide(self):
        result = self.tools.create_story_element(
            slide_id=self.slide.id,
            element_type="text",
            text="Texto criado pelo MCP",
            font_size_rem=1.2,
            font_weight=500,
            font_color="#123456",
            position="bottom",
            order=2,
        )

        element = StoryElement.objects.get(text="Texto criado pelo MCP")

        self.assertEqual(
            result,
            {
                "tool_response": (
                    f'Element {element.id} was created successfully on '
                    f'slide {self.slide.id} with the text: '
                    '"Texto criado pelo MCP".'
                ),
            },
        )
        self.assertEqual(element.variant, "#123456")
        self.assertEqual(element.position, "bottom")
        self.assertEqual(element.order, 2)

    def test_create_story_element_returns_error_for_unknown_slide(self):
        result = self.tools.create_story_element(
            slide_id=999999,
            element_type="text",
            text="Texto sem slide",
        )

        self.assertEqual(
            result,
            {"Error": "Slide id=999999 not found, try with other id"},
        )

    def test_update_story_element_persists_allowed_changes(self):
        element = StoryElement.objects.create(
            slide=self.slide,
            element_type=StoryElement.ElementType.TEXT,
            text="Texto antigo",
            order=1,
        )

        result = self.tools.update_story_element(
            element_id=element.id,
            changes={"text": "Texto atualizado", "order": 3},
        )

        element.refresh_from_db()

        self.assertEqual(result["element_id"], element.id)
        self.assertEqual(result["updated_fields"], ["text", "order"])
        self.assertEqual(element.text, "Texto atualizado")
        self.assertEqual(element.order, 3)

    def test_update_story_element_rejects_unknown_fields(self):
        element = StoryElement.objects.create(
            slide=self.slide,
            element_type=StoryElement.ElementType.TEXT,
            text="Texto",
        )

        with self.assertRaisesMessage(ValueError, "Campos não permitidos: title"):
            self.tools.update_story_element(
                element_id=element.id,
                changes={"title": "Não permitido"},
            )

    def test_update_story_persists_allowed_changes(self):
        result = self.tools.update_story(
            story_id=self.story.id,
            changes={
                "title": "Story MCP atualizado",
                "slug": "story-mcp-atualizado",
                "order": 6,
            },
        )

        self.story.refresh_from_db()

        self.assertEqual(result["updated_fields"], ["title", "slug", "order"])
        self.assertEqual(self.story.title, "Story MCP atualizado")
        self.assertEqual(self.story.slug, "story-mcp-atualizado")
        self.assertEqual(self.story.order, 6)

    def test_update_story_replaces_cover_and_returns_cover_url(self):
        image_base64 = self.make_png_base64()

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                result = self.tools.update_story(
                    story_id=self.story.id,
                    changes={"order": 9},
                    cover_base64=f"data:image/png;base64,{image_base64}",
                    cover_filename="C:\\uploads\\cover-tailandia.png",
                )

                self.story.refresh_from_db()

                self.assertEqual(
                    result["updated_fields"],
                    ["order", "cover"],
                )
                self.assertEqual(self.story.order, 9)
                self.assertTrue(self.story.cover.name.startswith("stories/cover/"))
                self.assertTrue(self.story.cover.name.endswith("cover-tailandia.png"))
                self.assertEqual(
                    result["cover_url"],
                    f"http://testserver/media/{self.story.cover.name}",
                )

    def test_create_story_creates_draft_with_cover_and_order(self):
        image_base64 = self.make_png_base64()

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                result = self.tools.create_story(
                    title="Ilhas imperdíveis da Tailândia",
                    slug="ilhas-imperdiveis-da-tailandia",
                    cover_base64=f"data:image/png;base64,{image_base64}",
                    cover_filename="C:\\uploads\\ilhas-tailandia.png",
                    order=3,
                )

                story = Story.objects.get(pk=result["story_id"])

                self.assertEqual(story.title, "Ilhas imperdíveis da Tailândia")
                self.assertEqual(story.slug, "ilhas-imperdiveis-da-tailandia")
                self.assertEqual(story.order, 3)
                self.assertFalse(story.is_published)
                self.assertNotIn("is_published", result)
                self.assertTrue(story.cover.name.startswith("stories/cover/"))
                self.assertTrue(
                    story.cover.name.endswith("ilhas-tailandia.png"),
                )
                self.assertEqual(
                    result["cover_url"],
                    f"http://testserver/media/{story.cover.name}",
                )

    def test_update_story_does_not_allow_publication_status(self):
        with self.assertRaisesMessage(
            ValueError,
            "Campos não permitidos: is_published",
        ):
            self.tools.update_story(
                story_id=self.story.id,
                changes={"is_published": False},
            )

    def test_create_story_slide_decodes_base64_and_persists_image(self):
        image_base64 = self.make_png_base64()

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                result = self.tools.create_story_slide(
                    story_id=self.story.id,
                    image_base64=f"data:image/png;base64,{image_base64}",
                    filename="C:\\uploads\\praia-khai-nai.png",
                    alt_text="Praia de Khai Nai Island com mar azul-turquesa.",
                    order=4,
                )

                slide = StorySlide.objects.get(pk=result["slide_id"])

                self.assertEqual(slide.story_id, self.story.id)
                self.assertEqual(
                    slide.alt_text,
                    "Praia de Khai Nai Island com mar azul-turquesa.",
                )
                self.assertEqual(slide.order, 4)
                self.assertTrue(slide.image.name.startswith("stories/slides/"))
                self.assertTrue(slide.image.name.endswith("praia-khai-nai.png"))
                self.assertEqual(
                    result["image_url"],
                    f"http://testserver/media/{slide.image.name}",
                )

    def test_create_story_slide_rejects_invalid_base64(self):
        with self.assertRaisesMessage(
            ValueError,
            "image_base64 não contém um Base64 válido.",
        ):
            self.tools.create_story_slide(
                story_id=self.story.id,
                image_base64="not-base64",
                filename="imagem.jpg",
                alt_text="Descrição válida",
            )

        self.assertEqual(self.story.slides.count(), 1)

    def test_create_story_slide_rejects_non_image_content(self):
        invalid_image = base64.b64encode(
            b"conteudo que nao e uma imagem",
        ).decode("ascii")

        with self.assertRaisesMessage(
            ValueError,
            "O conteúdo enviado não é uma imagem válida.",
        ):
            self.tools.create_story_slide(
                story_id=self.story.id,
                image_base64=invalid_image,
                filename="imagem.jpg",
                alt_text="Descrição válida",
            )

        self.assertEqual(self.story.slides.count(), 1)

    def test_update_story_slide_updates_metadata(self):
        result = self.tools.update_story_slide(
            slide_id=self.slide.id,
            alt_text="Praia atualizada",
            order=8,
            background_color="#112233",
        )

        self.slide.refresh_from_db()

        self.assertEqual(result["slide_id"], self.slide.id)
        self.assertEqual(
            result["updated_fields"],
            ["alt_text", "order", "background_color"],
        )
        self.assertEqual(self.slide.alt_text, "Praia atualizada")
        self.assertEqual(self.slide.order, 8)
        self.assertEqual(self.slide.background_color, "#112233")

    def test_update_story_slide_replaces_image(self):
        image_base64 = self.make_png_base64()

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                result = self.tools.update_story_slide(
                    slide_id=self.slide.id,
                    image_base64=image_base64,
                    filename="nova-praia.png",
                )

                self.slide.refresh_from_db()

                self.assertEqual(result["updated_fields"], ["image"])
                self.assertTrue(self.slide.image.name.endswith("nova-praia.png"))
                self.assertEqual(
                    result["image_url"],
                    f"http://testserver/media/{self.slide.image.name}",
                )

    def test_update_story_slide_requires_at_least_one_change(self):
        with self.assertRaisesMessage(
            ValueError,
            "Informe ao menos um campo para atualizar.",
        ):
            self.tools.update_story_slide(slide_id=self.slide.id)


class StoryFaviconTests(StoryTestCase):
    def setUp(self):
        super().setUp()
        self.site_setup = SiteSetup.objects.create(
            title="Ásia de Perto",
            description="Viagens pela Ásia.",
            favicon="assets/favicon/site.png",
            logo="assets/logo/site.png",
        )

    def test_favicon_is_rendered_on_landing_and_stories_list(self):
        landing_response = self.client.get(reverse("blog:landing"))
        stories_response = self.client.get(reverse("stories:list"))

        favicon_link = (
            '<link rel="icon" href="/media/assets/favicon/site.png" '
            'type="image/png">'
        )
        self.assertContains(landing_response, favicon_link, html=True)
        self.assertContains(stories_response, favicon_link, html=True)

    def test_favicon_is_rendered_when_opening_a_story(self):
        story = self.create_story(slug="story-com-favicon")
        self.create_slide(story)

        response = self.client.get(story.get_absolute_url())

        self.assertContains(
            response,
            '<link rel="icon" href="/media/assets/favicon/site.png" '
            'type="image/png">',
            html=True,
        )
