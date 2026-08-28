from django.contrib import admin
from site_setup.models import FooterSection, MenuLink, SiteSetup, SocialLink
# Register your models here.

# @admin.register(MenuLink)
# class MenuLinkAdmin(admin.ModelAdmin):
#     list_display = 'id', 'text', 'url_or_path',
#     list_display_links = 'id', 'text', 'url_or_path',
#     search_fields = 'id', 'text', 'url_or_path',

class FooterSectionInline(admin.TabularInline):
    model = FooterSection
    fields = 'title', 'order'
    extra = 1


class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    fields = (
        'text',
        'url_or_path',
        'new_tab',
        'placement',
        'footer_section',
        'order',
    )
    extra = 1


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1

@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description',
    inlines = FooterSectionInline, MenuLinkInline, SocialLinkInline
    
    def has_add_permission(self, request):
        return not SiteSetup.objects.exists()
