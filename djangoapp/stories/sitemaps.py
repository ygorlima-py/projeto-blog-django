from collections.abc import Iterable

from django.contrib.sitemaps import Sitemap

from stories.models import Story


class StorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self) -> Iterable:
        return Story.objects.filter(is_published=True)
    
    def lastmod(self, story):
        return story.updated_at