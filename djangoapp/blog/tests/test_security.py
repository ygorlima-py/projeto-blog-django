from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Page, Post


class RichTextSanitizationTests(TestCase):
    unsafe_content = (
        '<p onclick="alert(1)">Conteúdo <strong>seguro</strong></p>'
        '<script>alert("xss")</script>'
        '<a href="javascript:alert(1)">link perigoso</a>'
        '<img src="javascript:alert(1)" onerror="alert(1)">'
    )

    def test_post_content_removes_scripts_event_handlers_and_unsafe_urls(self):
        post = Post.objects.create(
            title='Post seguro',
            slug='post-seguro',
            excerpt='Resumo seguro.',
            content=self.unsafe_content,
        )

        self.assertIn('<p>Conteúdo <strong>seguro</strong></p>', post.content)
        self.assertNotIn('<script', post.content)
        self.assertNotIn('onclick=', post.content)
        self.assertNotIn('onerror=', post.content)
        self.assertNotIn('javascript:', post.content)

    def test_page_content_is_sanitized_before_being_rendered(self):
        page = Page.objects.create(
            title='Página segura',
            slug='pagina-segura',
            content=self.unsafe_content,
            is_published=True,
        )

        response = self.client.get(page.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<script')
        self.assertNotContains(response, 'onclick=')
        self.assertContains(response, 'Conteúdo')

    def test_template_sanitizes_content_changed_outside_model_save(self):
        post = Post.objects.create(
            title='Post legado',
            slug='post-legado',
            excerpt='Resumo seguro.',
            content='<p>Conteúdo inicial</p>',
            is_published=True,
        )
        Post.objects.filter(pk=post.pk).update(
            content='<p>Legado</p><script>alert("xss")</script>'
        )

        response = self.client.get(post.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<p>Legado</p>', html=True)
        self.assertNotContains(response, '<script')


class SummernoteUploadSecurityTests(TestCase):
    def setUp(self):
        self.upload_url = reverse('django_summernote-upload_attachment')

    def test_only_staff_users_can_access_summernote_upload_endpoint(self):
        anonymous_response = self.client.get(self.upload_url)
        regular_user = User.objects.create_user(
            username='leitor',
            password='senha-segura',
        )
        self.client.force_login(regular_user)
        regular_user_response = self.client.get(self.upload_url)

        staff_user = User.objects.create_user(
            username='editor',
            password='senha-segura',
            is_staff=True,
        )
        self.client.force_login(staff_user)
        staff_user_response = self.client.get(self.upload_url)

        self.assertEqual(anonymous_response.status_code, 302)
        self.assertEqual(regular_user_response.status_code, 403)
        self.assertEqual(staff_user_response.status_code, 400)

    def test_summernote_upload_limit_is_ten_megabytes(self):
        self.assertEqual(
            settings.SUMMERNOTE_CONFIG['attachment_filesize_limit'],
            10 * 1024 * 1024,
        )
