from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import AuthorProfile, Category, Post


class PostModelTests(TestCase):
    def create_post(self, **overrides):
        data = {
            'title': 'Vida na Tailândia',
            'excerpt': 'Relatos sobre a vida na Tailândia.',
            'content': '<p>Conteúdo de teste.</p>',
        }
        data.update(overrides)
        return Post.objects.create(**data)

    def test_reading_time_has_a_minimum_of_one_minute(self):
        post = self.create_post(content='')

        self.assertEqual(post.reading_time, 1)

    def test_reading_time_ignores_html_tags(self):
        content = f'<article><p>{"palavra " * 400}</p></article>'
        post = self.create_post(content=content)

        self.assertEqual(post.reading_time, 2)

    def test_featured_posts_are_listed_first(self):
        regular_post = self.create_post(title='Post comum')
        featured_post = self.create_post(title='Post em destaque', is_featured=True)

        self.assertEqual(
            list(Post.objects.get_published()),
            [featured_post, regular_post],
        )


class AuthorProfileTests(TestCase):
    def test_profile_is_created_with_user(self):
        user = User.objects.create_user(username='autor', password='senha-segura')

        self.assertTrue(AuthorProfile.objects.filter(user=user).exists())


class NavigationCategoriesTests(TestCase):
    def setUp(self):
        self.visible_category = Category.objects.create(
            name='Viagens',
            slug='viagens',
        )
        self.empty_category = Category.objects.create(
            name='Sem posts',
            slug='sem-posts',
        )
        Post.objects.create(
            title='Bangkok',
            slug='bangkok',
            excerpt='Primeiros dias em Bangkok.',
            content='Conteúdo',
            category=self.visible_category,
            is_published=True,
        )

    def test_only_categories_with_published_posts_are_available(self):
        response = self.client.get(reverse('blog:index'))

        categories = list(response.context['navigation_categories'])
        self.assertEqual(categories, [self.visible_category])
        self.assertNotIn(self.empty_category, categories)

    def test_reading_time_is_rendered_on_post_card(self):
        response = self.client.get(reverse('blog:index'))

        self.assertContains(response, '1 min de leitura')

    def test_category_filters_are_only_rendered_on_homepage(self):
        homepage_response = self.client.get(reverse('blog:index'))
        category_response = self.client.get(
            reverse('blog:category', args=(self.visible_category.slug,)),
        )

        self.assertContains(homepage_response, 'category-navigation-shell')
        self.assertNotContains(category_response, 'category-navigation-shell')
