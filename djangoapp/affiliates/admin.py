from django.contrib import admin
from django.utils.html import format_html

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
    list_display = ('cta_icon_preview','name', 'category', 'order', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('name', 'description')
    list_editable = ('order', 'is_published')
    autocomplete_fields = ('category',)
    ordering = ('order', 'name')
    readonly_fields = (
        "cta_icon_preview",
         "image_preview",
         )
    
    @admin.display(description="Ícone do CTA")
    def cta_icon_preview(self, obj):
        if not obj.cta_icon:
            return "Será gerado quando o parceiro for salvo."

        return format_html(
            '<img src="{}" width="48" height="48" '
            'style="object-fit: contain; border-radius: 50%;">',
            obj.cta_icon.url,
        )
        
    @admin.display(description="Prévia da imagem do afiliado")
    def image_preview(self, obj):
        if not obj.image:
            return "Nenhuma imagem cadastrada."
        
        return format_html(
            '<img src="{}" '
            'style="'
            'display:block;'
            'width:100%;'
            'max-width:320px;'
            'height:200px;'
            'object-fit:contain;'
            'border-radius:12px;'
            'background:#f1f1f1;'
            'padding:8px;'
            '">',
            obj.image.url,
        )
        
    