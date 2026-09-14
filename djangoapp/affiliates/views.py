from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from blog.seo import build_canonical_url

from .models import AffiliateCategory, AffiliatePartner


class AffiliateListView(ListView):
    model = AffiliatePartner
    template_name = 'affiliates/partner_list.html'
    context_object_name = 'partners'
    paginate_by = 12

    def get_active_category(self):
        if not hasattr(self, '_active_category'):
            category_slug = self.kwargs.get('category_slug')
            self._active_category = None

            if category_slug:
                self._active_category = get_object_or_404(
                    AffiliateCategory.objects.active(),
                    slug=category_slug,
                )

        return self._active_category

    def get_queryset(self):
        queryset = AffiliatePartner.objects.published().select_related(
            'category'
        )
        active_category = self.get_active_category()

        if active_category:
            queryset = queryset.filter(category=active_category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_category = self.get_active_category()
        context['categories'] = AffiliateCategory.objects.available()
        context['active_category'] = active_category

        if active_category:
            listing_title = active_category.name
            seo_title = active_category.name
            description = (
                f'Explore opções de {active_category.name}. Conheça os '
                'parceiros e acesse seus sites para consultar detalhes '
                'dos serviços.'
            )
            canonical_path = reverse(
                'affiliates:category', args=(active_category.slug,),
            )
        else:
            listing_title = 'Serviços'
            seo_title = 'Serviços para sua viagem'
            description = (
                'Encontre serviços de parceiros para planejar sua viagem: '
                'passagens aéreas, seguro viagem, eSIM, aluguel de veículos '
                'e transportes.'
            )
            canonical_path = reverse('affiliates:list')

        context.update({
            'listing_title': listing_title,
            'seo_title': seo_title,
            'meta_description': description,
            'canonical_url': build_canonical_url(
                self.request, canonical_path, context.get('page_obj'),
            ),
        })
        return context
