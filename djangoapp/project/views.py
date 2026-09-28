from django.http import HttpResponse
from django.urls import reverse


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(
        reverse('django.contrib.sitemaps.views.sitemap')
    )

    content = '\n'.join([
        'User-agent: OAI-SearchBot',
        'Disallow: /admin/',
        'Allow: /',
        '',
        'User-agent: *',
        'Disallow: /admin/',
        'Allow: /',
        '',
        f'Sitemap: {sitemap_url}',
    ])

    return HttpResponse(
        content,
        content_type='text/plain',
    )