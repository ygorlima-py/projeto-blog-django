from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse

from .models import AffiliateCategory, AffiliatePartner
from .views import AffiliateListView


class AffiliateModelsTests(TestCase):
    def setUp(self):
        self.category = AffiliateCategory.objects.create(
            name='Passagens',
            slug='passagens',
        )

    def make_partner(self, **overrides):
        data = {
            'category': self.category,
            'name': 'Parceiro de teste',
            'description': 'Descrição em texto simples.',
            'image_alt': 'Logotipo do parceiro de teste',
            'affiliate_url': 'https://example.com/oferta',
        }
        data.update(overrides)
        return AffiliatePartner(**data)

    def test_category_with_partner_is_protected_from_deletion(self):
        self.make_partner().save()

        with self.assertRaises(ProtectedError):
            self.category.delete()

    def test_description_rejects_html(self):
        partner = self.make_partner(description='<strong>Oferta</strong>')

        with self.assertRaises(ValidationError) as error:
            partner.full_clean(exclude=('image',))

        self.assertIn('description', error.exception.message_dict)

    def test_affiliate_url_rejects_non_https_links(self):
        partner = self.make_partner(affiliate_url='http://example.com/oferta')

        with self.assertRaises(ValidationError) as error:
            partner.full_clean(exclude=('image',))

        self.assertIn('affiliate_url', error.exception.message_dict)

    def test_affiliate_url_accepts_https_links(self):
        partner = self.make_partner()

        partner.full_clean(exclude=('image',))

    def test_category_rejects_unsafe_svg_icon(self):
        self.category.icon = SimpleUploadedFile(
            'unsafe.svg',
            b'<svg xmlns="http://www.w3.org/2000/svg">'
            b'<script>alert(1)</script></svg>',
            content_type='image/svg+xml',
        )

        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_published_queryset_hides_drafts_and_inactive_categories(self):
        published_partner = self.make_partner(
            name='Publicado',
            is_published=True,
        )
        published_partner.save()
        self.make_partner(name='Rascunho').save()

        inactive_category = AffiliateCategory.objects.create(
            name='Inativa',
            slug='inativa',
            is_active=False,
        )
        self.make_partner(
            category=inactive_category,
            name='Publicado em categoria inativa',
            is_published=True,
        ).save()

        self.assertQuerySetEqual(
            AffiliatePartner.objects.published(),
            [published_partner],
        )

    def test_available_categories_hide_inactive_and_empty_categories(self):
        self.make_partner(is_published=True).save()
        AffiliateCategory.objects.create(
            name='Sem parceiros publicados',
            slug='sem-parceiros-publicados',
        )
        inactive_category = AffiliateCategory.objects.create(
            name='Inativa',
            slug='inativa',
            is_active=False,
        )
        self.make_partner(
            category=inactive_category,
            name='Parceiro em categoria inativa',
            is_published=True,
        ).save()

        self.assertQuerySetEqual(
            AffiliateCategory.objects.available(),
            [self.category],
        )


class AffiliateListViewTests(TestCase):
    def setUp(self):
        self.category = AffiliateCategory.objects.create(
            name='Passagens',
            slug='passagens',
        )

    def make_partner(self, **overrides):
        data = {
            'category': self.category,
            'name': 'Parceiro de teste',
            'description': 'Descrição em texto simples.',
            'image_alt': 'Logotipo do parceiro de teste',
            'affiliate_url': 'https://example.com/oferta',
            'is_published': True,
        }
        data.update(overrides)
        return AffiliatePartner.objects.create(**data)

    def test_public_list_contains_only_published_partners_from_active_categories(
        self,
    ):
        published_partner = self.make_partner(name='Publicado')
        self.make_partner(name='Rascunho', is_published=False)
        inactive_category = AffiliateCategory.objects.create(
            name='Inativa',
            slug='inativa',
            is_active=False,
        )
        self.make_partner(
            category=inactive_category,
            name='Parceiro em categoria inativa',
        )

        response = self.client.get(reverse('affiliates:list'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context_data['partners'],
            [published_partner],
        )

    def test_category_route_filters_partners_and_sets_active_category(self):
        selected_partner = self.make_partner(name='Parceiro selecionado')
        other_category = AffiliateCategory.objects.create(
            name='Hospedagem',
            slug='hospedagem',
        )
        self.make_partner(
            category=other_category,
            name='Parceiro de outra categoria',
        )

        response = self.client.get(
            reverse(
                'affiliates:category',
                kwargs={'category_slug': self.category.slug},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context_data['partners'],
            [selected_partner],
        )
        self.assertEqual(
            response.context_data['active_category'],
            self.category,
        )
        self.assertQuerySetEqual(
            response.context_data['categories'],
            [other_category, self.category],
            ordered=False,
        )

    def test_inactive_category_returns_404(self):
        category = AffiliateCategory.objects.create(
            name='Inativa',
            slug='inativa',
            is_active=False,
        )

        response = self.client.get(
            reverse(
                'affiliates:category',
                kwargs={'category_slug': category.slug},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_unknown_category_returns_404(self):
        response = self.client.get(
            reverse(
                'affiliates:category',
                kwargs={'category_slug': 'categoria-inexistente'},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_view_paginates_twelve_partners_per_page(self):
        self.assertEqual(AffiliateListView.paginate_by, 12)

    def test_list_page_renders_empty_state(self):
        response = self.client.get(reverse('affiliates:list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'affiliates/partner_list.html',
        )
        self.assertContains(response, 'Nenhum parceiro encontrado')

    def test_partner_link_is_rendered_as_sponsored_external_link(self):
        partner = self.make_partner()

        response = self.client.get(reverse('affiliates:list'))

        self.assertContains(response, partner.name)
        self.assertContains(response, 'target="_blank"')
        self.assertContains(
            response,
            'rel="sponsored noopener noreferrer"',
        )

    def test_public_page_renders_published_partner_and_hides_draft(self):
        published_partner = self.make_partner(name='Parceiro publicado')
        draft_partner = self.make_partner(
            name='Parceiro em rascunho',
            is_published=False,
        )

        response = self.client.get(reverse('affiliates:list'))

        self.assertContains(response, published_partner.name)
        self.assertNotContains(response, draft_partner.name)

    def test_categories_respect_configured_order(self):
        self.category.order = 20
        self.category.save(update_fields=('order',))
        self.make_partner(category=self.category)
        first_category = AffiliateCategory.objects.create(
            name='Primeira categoria',
            slug='primeira-categoria',
            order=1,
        )
        self.make_partner(
            category=first_category,
            name='Parceiro da primeira categoria',
        )

        response = self.client.get(reverse('affiliates:list'))

        self.assertQuerySetEqual(
            response.context_data['categories'],
            [first_category, self.category],
        )

    def test_category_icon_is_rendered_in_filter_and_partner_card(self):
        self.category.icon = 'affiliates/category-icons/insurance.svg'
        self.category.save(update_fields=('icon',))
        self.make_partner()

        response = self.client.get(reverse('affiliates:list'))

        self.assertContains(
            response,
            '/media/affiliates/category-icons/insurance.svg',
            count=1,
        )

    def test_partners_respect_configured_order(self):
        last_partner = self.make_partner(
            name='Último parceiro',
            order=20,
        )
        first_partner = self.make_partner(
            name='Primeiro parceiro',
            order=1,
        )

        response = self.client.get(reverse('affiliates:list'))

        self.assertQuerySetEqual(
            response.context_data['partners'],
            [first_partner, last_partner],
        )

    def test_description_is_escaped_in_public_html(self):
        unsafe_description = '<script>alert("xss")</script>'
        self.make_partner(description=unsafe_description)

        response = self.client.get(reverse('affiliates:list'))

        self.assertNotContains(response, unsafe_description)
        self.assertContains(
            response,
            '&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;',
        )

    def test_sitemap_contains_only_available_affiliate_categories(self):
        self.make_partner()
        empty_category = AffiliateCategory.objects.create(
            name='Sem parceiros',
            slug='sem-parceiros',
        )
        draft_category = AffiliateCategory.objects.create(
            name='Somente rascunhos',
            slug='somente-rascunhos',
        )
        self.make_partner(
            category=draft_category,
            name='Parceiro não publicado',
            is_published=False,
        )
        inactive_category = AffiliateCategory.objects.create(
            name='Inativa',
            slug='inativa',
            is_active=False,
        )
        self.make_partner(
            category=inactive_category,
            name='Parceiro em categoria inativa',
        )

        response = self.client.get('/sitemap.xml')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/parceiros/</loc>')
        self.assertContains(response, '/parceiros/categoria/passagens/</loc>')
        self.assertNotContains(
            response,
            f'/parceiros/categoria/{empty_category.slug}/',
        )
        self.assertNotContains(
            response,
            f'/parceiros/categoria/{draft_category.slug}/',
        )
        self.assertNotContains(
            response,
            f'/parceiros/categoria/{inactive_category.slug}/',
        )
