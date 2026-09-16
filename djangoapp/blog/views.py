import json
from typing import Any

from django.shortcuts import render, redirect

from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models.query import QuerySet
from django.views.generic.base import TemplateView

from blog.models import Post, Page
from blog.seo import build_canonical_url
from site_setup.models import SiteSetup
from affiliates.models import AffiliateCategory
from stories.models import Story


'''
Views de exibição genéricas

É uma lista? ou em um único objeto só?

Se for lista  use ListView
Se for um único objeto só use DetailView

Para mais detalhes consulte: https://docs.djangoproject.com/pt-br/4.2/ref/class-based-views
'''

POSTS_PER_PAGE = 9

class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html' 
    context_object_name = 'posts'
    ordering = '-pk',
    paginate_by = POSTS_PER_PAGE
    queryset = Post.objects.get_published() #type: ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'home - ',
            'listing_eyebrow': 'Diário de viagem',
            'listing_title': 'Histórias mais recentes',
        })
        if self.request.resolver_match.view_name == 'blog:index':
            context.update({
                'seo_title': 'Viagem e vida na Ásia',
                'meta_description': (
                    'Custos, vistos e dicas para viajar e morar na Ásia, com '
                    'relatos de quem vive na região.'
                ),
                'canonical_url': build_canonical_url(
                    self.request,
                    reverse('blog:index'),
                    context.get('page_obj'),
                ),
            })
        return context

class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username
    
        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'

        page_title = f'Posts de {user_full_name} - '

        context.update({
            'page_title': page_title,
            'listing_eyebrow': 'Autor',
            'listing_title': f'Histórias de {user_full_name}',
        })

        return context

    def get_queryset(self, **kwargs) -> dict[str, Any]:
        qs = super().get_queryset()

        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)

        return qs #type: ignore
    
    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()
        
        self._temp_context.update({'author_pk': author_pk, 'user': user,})
        
        
        return super().get(request, *args, **kwargs)
        
class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        qs = super().get_queryset()
        qs = qs.filter(category__slug=slug)

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_name = self.object_list[0].category.name # type: ignore 
        page_title = f'{category_name} - Categoria - '
        context.update({
            'page_title': page_title,
            'listing_eyebrow': 'Categoria',
            'listing_title': category_name,
        })

        return context

class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        self.slug = self.kwargs.get('slug')
        qs = super().get_queryset()
        qs = qs.filter(tags__slug=self.slug)

        return qs
    
    def get_context_data(self, **kwargs)-> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tag_name = self.object_list[0].tags.filter(slug=self.slug).first() # type: ignore
        page_title = f'{tag_name} - Tag - '
        context.update({
            'page_title': page_title,
            'listing_eyebrow': 'Tag',
            'listing_title': str(tag_name),
        })

        return context

class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value) 
        )[:POSTS_PER_PAGE]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self._search_value
        context.update({
            'page_title': f'{self._search_value[:30]} - search',
            'search_value': search_value,
            'listing_eyebrow': 'Busca',
            'listing_title': f'Resultados para “{search_value}”',
        })
        return context
    
    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        contexto = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f'{page.title} - Página -' #type: ignore
        contexto.update({
            'page_title': page_title,
        })

        if page.slug == 'passagens-aereas':
            contexto.update({
                'seo_title': page.title,
                'meta_description': (
                    'Pesquise e compare passagens aéreas para destinos no '
                    'mundo todo. Consulte opções de voos e conclua sua '
                    'reserva no site do parceiro.'
                ),
                'canonical_url': build_canonical_url(
                    self.request, page.get_absolute_url(),
                ),
            })

        return contexto
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    slug_field = 'slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        contexto = super().get_context_data(**kwargs)
        post = self.object
        page_title = f'{post.title} - Post -' #type: ignore

        post_url = self.request.build_absolute_uri(post.get_absolute_url())
        homepage_url = self.request.build_absolute_uri('/')
        site_setup = SiteSetup.objects.order_by('-id').first()
        publisher_name = site_setup.title if site_setup else 'Ásia de Perto'

        publisher: dict[str, Any] = {
            '@type': 'Organization',
            'name': publisher_name,
            'url': homepage_url,
        }

        if site_setup and site_setup.logo:
            publisher['logo'] = {
                '@type': 'ImageObject',
                'url': self.request.build_absolute_uri(site_setup.logo.url),
            }

        blogposting_schema: dict[str, Any] = {
            '@context': 'https://schema.org',
            '@type': 'BlogPosting',
            'mainEntityOfPage': {
                '@type': 'WebPage',
                '@id': post_url,
            },
            'url': post_url,
            'headline': post.title,
            'description': strip_tags(post.excerpt),
            'datePublished': post.created_at.isoformat(),
            'dateModified': post.updated_at.isoformat(),
            'publisher': publisher,
            'inLanguage': 'pt-BR',
        }

        if post.created_by:
            author_name = (
                post.created_by.get_full_name().strip()
                or post.created_by.get_username()
            )
            blogposting_schema['author'] = {
                '@type': 'Person',
                'name': author_name,
                'url': self.request.build_absolute_uri(
                    reverse('blog:created_by', args=(post.created_by.pk,)),
                ),
            }

        if post.cover:
            blogposting_schema['image'] = [
                self.request.build_absolute_uri(post.cover.url),
            ]

        blogposting_schema_json = (
            json.dumps(blogposting_schema, ensure_ascii=False)
            .replace('&', '\\u0026')
            .replace('<', '\\u003c')
            .replace('>', '\\u003e')
        )

        contexto.update({
            'page_title': page_title,
            'blogposting_schema': blogposting_schema_json,
        })

        return contexto

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)

class LandingPageView(TemplateView):
    template_name = "blog/pages/landing.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        context["affiliate_categories"] = AffiliateCategory.objects.available()
        context["stories"] = Story.objects.filter(is_published=True).order_by("order", "title")
        
        return context
    

    