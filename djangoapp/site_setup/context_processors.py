from django.db.models import Prefetch

from site_setup.models import FooterSection, MenuLink, SiteSetup

def context_processor_example(request):
    return {
        'example': 'Isto aqui Veio do Context Processors'
    }

def site_setup(request):
    setup = SiteSetup.objects.order_by('-id').first()
    footer_sections = ()
    uncategorized_footer_links = ()

    if setup:
        footer_links = MenuLink.objects.filter(
            site_setup=setup,
            placement__in=(
                MenuLink.Placement.BOTH,
                MenuLink.Placement.FOOTER,
            ),
        ).order_by('order', 'pk')

        footer_sections = FooterSection.objects.filter(
            site_setup=setup,
        ).prefetch_related(
            Prefetch(
                'links',
                queryset=footer_links,
                to_attr='footer_links',
            ),
        )
        uncategorized_footer_links = footer_links.filter(
            footer_section__isnull=True,
        )

    return {
        'site_setup': setup,
        'footer_sections': footer_sections,
        'uncategorized_footer_links': uncategorized_footer_links,
    }
