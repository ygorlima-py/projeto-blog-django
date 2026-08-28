from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import AffiliateCategory


class AffiliateListSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return ['affiliates:list']

    def location(self, item):
        return reverse(item)


class AffiliateCategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return AffiliateCategory.objects.available()

    def location(self, category):
        return reverse(
            'affiliates:category',
            kwargs={'category_slug': category.slug},
        )
