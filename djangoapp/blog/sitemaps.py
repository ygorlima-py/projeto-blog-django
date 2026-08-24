from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Page, Post


class StaticSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return ['blog:index']

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Post.objects.get_published()

    def lastmod(self, post):
        return post.updated_at


class PageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Page.objects.filter(is_published=True).order_by('pk')
