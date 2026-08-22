from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from site_setup.models import MenuLink, SiteSetup, SocialLink


class SocialLinkTests(TestCase):
    def setUp(self):
        self.site_setup = SiteSetup.objects.create(
            title='Rota Asiática',
            description='Vida e viagens pela Tailândia.',
        )

    def test_custom_label_is_used_as_display_name(self):
        social_link = SocialLink.objects.create(
            site_setup=self.site_setup,
            platform=SocialLink.Platform.INSTAGRAM,
            label='Siga no Instagram',
            url='https://www.instagram.com/rotaasiatica/',
        )

        self.assertEqual(social_link.display_name, 'Siga no Instagram')
        self.assertEqual(social_link.icon_class, 'fa-brands fa-instagram')

    def test_platform_name_is_the_fallback(self):
        social_link = SocialLink.objects.create(
            site_setup=self.site_setup,
            platform=SocialLink.Platform.YOUTUBE,
            url='https://www.youtube.com/',
        )

        self.assertEqual(social_link.display_name, 'YouTube')


class DynamicSiteIdentityTests(TestCase):
    def test_site_title_and_description_come_from_site_setup(self):
        SiteSetup.objects.create(
            title='Nome editável',
            description='Descrição editável pelo painel.',
        )

        response = self.client.get(reverse('blog:index'))

        self.assertContains(response, 'Nome editável')
        self.assertContains(response, 'Descrição editável pelo painel.')


class DynamicMenuTests(TestCase):
    def test_menu_link_created_in_admin_is_rendered_in_header_and_footer(self):
        site_setup = SiteSetup.objects.create(
            title='Rota Asiática',
            description='Vida e viagens pela Tailândia.',
        )
        menu_link = MenuLink.objects.create(
            site_setup=site_setup,
            text='Vistos',
            url_or_path='/category/vistos/',
        )

        response = self.client.get(reverse('blog:index'))

        self.assertContains(response, menu_link.text, count=2)
        self.assertContains(response, f'href="{menu_link.url_or_path}"', count=2)

    def test_footer_only_link_is_not_rendered_in_header(self):
        site_setup = SiteSetup.objects.create(
            title='Rota Asiática',
            description='Vida e viagens pela Tailândia.',
        )
        menu_link = MenuLink.objects.create(
            site_setup=site_setup,
            text='Política de Privacidade',
            url_or_path='/page/politica-de-privacidade/',
            placement=MenuLink.Placement.FOOTER,
        )

        response = self.client.get(reverse('blog:index'))

        self.assertContains(response, menu_link.text, count=1)
        self.assertContains(response, f'href="{menu_link.url_or_path}"', count=1)

    def test_menu_rejects_javascript_and_unencrypted_external_urls(self):
        invalid_links = (
            'javascript:alert(1)',
            'http://example.com',
            '//example.com',
            '/\\example.com',
        )

        for url_or_path in invalid_links:
            with self.subTest(url_or_path=url_or_path):
                menu_link = MenuLink(text='Link inseguro', url_or_path=url_or_path)
                with self.assertRaises(ValidationError):
                    menu_link.full_clean()

    def test_menu_accepts_internal_paths_anchors_and_https_urls(self):
        valid_links = ('/category/vistos/', '#top', 'https://www.instagram.com/')

        for url_or_path in valid_links:
            with self.subTest(url_or_path=url_or_path):
                menu_link = MenuLink(text='Link seguro', url_or_path=url_or_path)
                menu_link.full_clean()
