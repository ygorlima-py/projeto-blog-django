from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Page, Post
from blog.security import (
    TRAVELPAYOUTS_WIDGET_ATTRIBUTE,
    is_allowed_travelpayouts_widget_url,
    sanitize_rich_text,
)


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
        self.assertNotContains(response, '<script>alert("xss")</script>')
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
        self.assertNotContains(response, '<script>alert("xss")</script>')

    def test_valid_travelpayouts_widget_marker_survives_sanitization(self):
        widget_url = (
            'https://tpemd.com/content?currency=usd&campaign_id=111'
            '&future_parameter=kept'
        )
        content = (
            '<div class="travelpayouts-widget" '
            f'{TRAVELPAYOUTS_WIDGET_ATTRIBUTE}="'
            f'{widget_url.replace("&", "&amp;")}"></div>'
        )

        post = Post.objects.create(
            title='Post com widget',
            slug='post-com-widget',
            excerpt='Resumo seguro.',
            content=content,
            is_published=True,
        )
        response = self.client.get(post.get_absolute_url())

        self.assertIn('class="travelpayouts-widget"', post.content)
        self.assertIn(
            f'{TRAVELPAYOUTS_WIDGET_ATTRIBUTE}="'
            'https://tpemd.com/content?currency=usd&amp;campaign_id=111'
            '&amp;future_parameter=kept"',
            post.content,
        )
        self.assertContains(response, 'future_parameter=kept')

    def test_travelpayouts_widget_url_validation_rejects_bypasses(self):
        invalid_urls = (
            'http://tpemd.com/content?campaign_id=111',
            'https://evil-tpemd.com/content?campaign_id=111',
            'https://tpemd.com.evil.example/content?campaign_id=111',
            'https://tpemd.com@evil.example/content?campaign_id=111',
            'https://user:password@tpemd.com/content?campaign_id=111',
            'https://tpemd.com:8443/content?campaign_id=111',
            'https://tpemd.com/other-path?campaign_id=111',
            'https://tpemd.com/content?campaign_id=111#fragment',
            'https:\\tpemd.com/content?campaign_id=111',
            ' https://tpemd.com/content?campaign_id=111',
            'javascript:alert(1)',
        )

        for widget_url in invalid_urls:
            with self.subTest(widget_url=widget_url):
                self.assertFalse(
                    is_allowed_travelpayouts_widget_url(widget_url),
                )

                sanitized = sanitize_rich_text(
                    '<div class="travelpayouts-widget" '
                    f'{TRAVELPAYOUTS_WIDGET_ATTRIBUTE}="{widget_url}"></div>',
                )
                self.assertNotIn(TRAVELPAYOUTS_WIDGET_ATTRIBUTE, sanitized)

    def test_travelpayouts_widget_url_accepts_arbitrary_query_parameters(self):
        widget_url = (
            'https://tpemd.com/content?campaign_id=999&promo_id=4563'
            '&from_name=GRU&to_name=bangkok_th&new_option=value%2Ffuture'
        )

        self.assertTrue(is_allowed_travelpayouts_widget_url(widget_url))


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
