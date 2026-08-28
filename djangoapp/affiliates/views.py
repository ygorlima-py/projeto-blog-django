from django.shortcuts import get_object_or_404
from django.views.generic import ListView

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
        context['categories'] = AffiliateCategory.objects.available()
        context['active_category'] = self.get_active_category()
        return context
