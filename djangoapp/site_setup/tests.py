from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from site_setup.models import FooterSection, MenuLink, SiteSetup, SocialLink


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

    def test_uploaded_logo_replaces_the_fallback_compass(self):
        SiteSetup.objects.create(
            title='Descubra Ásia',
            description='Vida e viagens pela Ásia.',
            logo='assets/logo/2026/08/logo.png',
        )

        response = self.client.get(reverse('blog:index'))

        self.assertContains(
            response,
            'src="/media/assets/logo/2026/08/logo.png"',
            count=2,
        )
        self.assertNotContains(response, 'viewBox="0 0 48 48"')


class DynamicMenuTests(TestCase):
    def test_footer_groups_and_links_follow_configured_order(self):
        site_setup = SiteSetup.objects.create(
            title='Rota Asiática',
            description='Vida e viagens pela Tailândia.',
        )
        second_section = FooterSection.objects.create(
            site_setup=site_setup,
            title='Guias',
            order=20,
        )
        first_section = FooterSection.objects.create(
            site_setup=site_setup,
            title='Planeje sua viagem',
            order=10,
        )
        MenuLink.objects.create(
            site_setup=site_setup,
            footer_section=first_section,
            text='Hotéis',
            url_or_path='/hoteis/',
            placement=MenuLink.Placement.FOOTER,
            order=20,
        )
        MenuLink.objects.create(
            site_setup=site_setup,
            footer_section=first_section,
            text='Passagens aéreas',
            url_or_path='/pagina/passagens-aereas/',
            placement=MenuLink.Placement.FOOTER,
            order=10,
        )
        MenuLink.objects.create(
            site_setup=site_setup,
            footer_section=second_section,
            text='Roteiros',
            url_or_path='/roteiros/',
            placement=MenuLink.Placement.FOOTER,
            order=10,
        )

        response = self.client.get(reverse('blog:index'))
        content = response.content.decode()

        self.assertLess(
            content.find('Planeje sua viagem'),
            content.find('Passagens aéreas'),
        )
        self.assertLess(content.find('Passagens aéreas'), content.find('Hotéis'))
        self.assertLess(content.find('Hotéis'), content.find('Guias'))
        self.assertLess(content.find('Guias'), content.find('Roteiros'))
        self.assertNotContains(response, '>Explore<')

    def test_uncategorized_footer_links_remain_in_explore(self):
        site_setup = SiteSetup.objects.create(
            title='Rota Asiática',
            description='Vida e viagens pela Tailândia.',
        )
        menu_link = MenuLink.objects.create(
            site_setup=site_setup,
            text='Sobre',
            url_or_path='/pagina/sobre/',
            placement=MenuLink.Placement.FOOTER,
        )

        response = self.client.get(reverse('blog:index'))

        self.assertContains(response, '>Explore<')
        self.assertContains(response, menu_link.text)

    def test_menu_links_follow_configured_order_in_header_and_footer(self):
        site_setup = SiteSetup.objects.create(
            title='Rota Asiática',
            description='Vida e viagens pela Tailândia.',
        )
        MenuLink.objects.create(
            site_setup=site_setup,
            text='Segundo link',
            url_or_path='/segundo/',
            order=20,
        )
        MenuLink.objects.create(
            site_setup=site_setup,
            text='Primeiro link',
            url_or_path='/primeiro/',
            order=10,
        )

        response = self.client.get(reverse('blog:index'))
        content = response.content.decode()

        self.assertLess(content.find('Primeiro link'), content.find('Segundo link'))
        self.assertLess(content.rfind('Primeiro link'), content.rfind('Segundo link'))

    def test_menu_link_created_in_admin_is_rendered_in_header_and_footer(self):
        site_setup = SiteSetup.objects.create(
            title='Rota Asiática',
            description='Vida e viagens pela Tailândia.',
        )
        menu_link = MenuLink.objects.create(
            site_setup=site_setup,
            text='Vistos',
            url_or_path='/categoria/vistos/',
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
            url_or_path='/pagina/politica-de-privacidade/',
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
        valid_links = ('/categoria/vistos/', '#top', 'https://www.instagram.com/')

        for url_or_path in valid_links:
            with self.subTest(url_or_path=url_or_path):
                menu_link = MenuLink(text='Link seguro', url_or_path=url_or_path)
                menu_link.full_clean()
