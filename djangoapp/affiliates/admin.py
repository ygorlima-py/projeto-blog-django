from django.contrib import admin

from .models import AffiliateCategory, AffiliatePartner


@admin.register(AffiliateCategory)
class AffiliateCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    ordering = ('order', 'name')


@admin.register(AffiliatePartner)
class AffiliatePartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('name', 'description')
    list_editable = ('order', 'is_published')
    autocomplete_fields = ('category',)
    ordering = ('order', 'name')
