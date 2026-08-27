from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Category, Page, Post, Tag
from blog.views import POSTS_PER_PAGE


class PublicBlogViewsTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='autor',
            first_name='Ygor',
            last_name='Lima',
            password='senha-segura',
        )
        self.other_author = User.objects.create_user(
            username='outro-autor',
            password='senha-segura',
        )
        self.category = Category.objects.create(name='Vistos', slug='vistos')
        self.tag = Tag.objects.create(name='DTV', slug='dtv')

    def create_post(self, **overrides):
        sequence = Post.objects.count() + 1
        data = {
            'title': f'Post público {sequence}',
            'slug': f'post-publico-{sequence}',
            'excerpt': 'Resumo do post de teste.',
            'content': 'Conteúdo do post de teste.',
            'created_by': self.author,
            'category': self.category,
            'is_published': True,
        }
        data.update(overrides)
        post = Post.objects.create(**data)
        post.tags.add(self.tag)
        return post

    def test_homepage_lists_only_published_posts(self):
        published_post = self.create_post(title='Post publicado', slug='post-publicado')
        draft_post = self.create_post(
            title='Rascunho privado',
            slug='rascunho-privado',
            is_published=False,
        )

        response = self.client.get(reverse('blog:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, published_post.title)
        self.assertNotContains(response, draft_post.title)

    def test_post_detail_is_available_only_when_published(self):
        published_post = self.create_post(title='Post visível', slug='post-visivel')
        draft_post = self.create_post(
            title='Post oculto',
            slug='post-oculto',
            is_published=False,
        )

        published_response = self.client.get(published_post.get_absolute_url())
        draft_response = self.client.get(f'/post/{draft_post.slug}/')

        self.assertEqual(published_response.status_code, 200)
        self.assertTemplateUsed(published_response, 'blog/pages/post.html')
        self.assertContains(published_response, published_post.title)
        self.assertEqual(draft_response.status_code, 404)

    def test_post_detail_has_social_sharing_links_and_metadata(self):
        post = self.create_post(
            title='Guia para compartilhar',
            slug='guia-para-compartilhar',
        )

        response = self.client.get(post.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-share-bar')
        self.assertContains(response, 'data-share-url="http://testserver')
        self.assertContains(response, 'facebook.com/sharer/sharer.php')
        self.assertContains(response, 'twitter.com/intent/tweet')
        self.assertContains(response, 'linkedin.com/sharing/share-offsite')
        self.assertContains(response, 'wa.me/')
        self.assertContains(response, 'fa-brands fa-instagram')
        self.assertContains(response, 'property="og:type" content="article"')
        self.assertContains(response, f'property="og:title" content="{post.title}"')

    def test_post_detail_loads_travelpayouts_widget_loader(self):
        post = self.create_post()

        response = self.client.get(post.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '/static/blog/javascript/travelpayouts_widgets.js',
        )

    def test_page_detail_is_available_only_when_published(self):
        published_page = Page.objects.create(
            title='Sobre mim',
            slug='sobre-mim',
            content='Página pública.',
            is_published=True,
        )
        draft_page = Page.objects.create(
            title='Rascunho de página',
            slug='rascunho-de-pagina',
            content='Página privada.',
            is_published=False,
        )

        published_response = self.client.get(published_page.get_absolute_url())
        draft_response = self.client.get(f'/pagina/{draft_page.slug}/')

        self.assertEqual(published_response.status_code, 200)
        self.assertTemplateUsed(published_response, 'blog/pages/page.html')
        self.assertContains(published_response, published_page.title)
        self.assertEqual(draft_response.status_code, 404)

        legacy_response = self.client.get(f'/page/{published_page.slug}/')
        self.assertRedirects(
            legacy_response,
            published_page.get_absolute_url(),
            status_code=301,
            target_status_code=200,
        )

    def test_category_and_tag_pages_hide_unpublished_posts(self):
        published_post = self.create_post(title='Visto publicado', slug='visto-publicado')
        draft_post = self.create_post(
            title='Visto em rascunho',
            slug='visto-em-rascunho',
            is_published=False,
        )

        category_response = self.client.get(
            reverse('blog:category', args=(self.category.slug,)),
        )
        tag_response = self.client.get(reverse('blog:tag', args=(self.tag.slug,)))

        for response in (category_response, tag_response):
            with self.subTest(url=response.request['PATH_INFO']):
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, published_post.title)
                self.assertNotContains(response, draft_post.title)

        legacy_category_response = self.client.get(
            f'/category/{self.category.slug}/',
        )
        self.assertRedirects(
            legacy_category_response,
            reverse('blog:category', args=(self.category.slug,)),
            status_code=301,
            target_status_code=200,
        )

    def test_author_page_shows_only_the_authors_published_posts(self):
        author_post = self.create_post(title='Post do autor', slug='post-do-autor')
        self.create_post(
            title='Rascunho do autor',
            slug='rascunho-do-autor',
            is_published=False,
        )
        other_post = self.create_post(
            title='Post de outro autor',
            slug='post-de-outro-autor',
            created_by=self.other_author,
        )

        response = self.client.get(reverse('blog:created_by', args=(self.author.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, author_post.title)
        self.assertNotContains(response, 'Rascunho do autor')
        self.assertNotContains(response, other_post.title)

    def test_search_finds_title_excerpt_and_content_of_published_posts(self):
        title_post = self.create_post(
            title='Guia de Chiang Mai',
            slug='guia-chiang-mai',
        )
        excerpt_post = self.create_post(
            title='Outro assunto',
            slug='outro-assunto',
            excerpt='Hospedagem perto do rio Kwai.',
        )
        content_post = self.create_post(
            title='Mais um assunto',
            slug='mais-um-assunto',
            content='Como solicitar o visto DTV.',
        )
        draft_post = self.create_post(
            title='Guia secreto de Chiang Mai',
            slug='guia-secreto',
            is_published=False,
        )

        cases = (
            ('Chiang Mai', title_post.title),
            ('rio Kwai', excerpt_post.title),
            ('visto DTV', content_post.title),
        )

        for search_value, expected_title in cases:
            with self.subTest(search_value=search_value):
                response = self.client.get(
                    reverse('blog:search'),
                    {'search': search_value},
                )

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, expected_title)
                self.assertNotContains(response, draft_post.title)

    def test_empty_search_redirects_to_homepage(self):
        response = self.client.get(reverse('blog:search'), {'search': '   '})

        self.assertRedirects(response, reverse('blog:index'))

    def test_index_is_paginated_after_nine_posts(self):
        for position in range(POSTS_PER_PAGE + 1):
            self.create_post(
                title=f'Post paginado {position}',
                slug=f'post-paginado-{position}',
            )

        first_page_response = self.client.get(reverse('blog:index'))
        second_page_response = self.client.get(reverse('blog:index'), {'page': 2})

        self.assertEqual(len(first_page_response.context['page_obj'].object_list), POSTS_PER_PAGE)
        self.assertTrue(first_page_response.context['page_obj'].has_next())
        self.assertEqual(len(second_page_response.context['page_obj'].object_list), 1)

    def test_unknown_public_urls_return_404(self):
        urls = (
            reverse('blog:post', args=('post-inexistente',)),
            reverse('blog:page', args=('pagina-inexistente',)),
            reverse('blog:category', args=('categoria-inexistente',)),
            reverse('blog:tag', args=('tag-inexistente',)),
            reverse('blog:created_by', args=(99999,)),
        )

        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_sitemap_contains_only_public_content(self):
        published_post = self.create_post(
            title='Post no sitemap',
            slug='post-no-sitemap',
        )
        self.create_post(
            title='Rascunho fora do sitemap',
            slug='rascunho-fora-do-sitemap',
            is_published=False,
        )
        published_page = Page.objects.create(
            title='Página no sitemap',
            slug='pagina-no-sitemap',
            content='Conteúdo público.',
            is_published=True,
        )

        response = self.client.get('/sitemap.xml')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertContains(response, published_post.get_absolute_url())
        self.assertContains(response, published_page.get_absolute_url())
        self.assertNotContains(response, 'rascunho-fora-do-sitemap')
