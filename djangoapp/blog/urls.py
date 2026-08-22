from django.urls import path
from django.views.generic.base import RedirectView
from blog.views import (
                        PostListView, 
                        PageDetailView, 
                        PostDetailView, 
                        CreatedByListView, 
                        CategoryListView, 
                        TagListView, 
                        SearchListView,
                        )


# Para mais detalhes sobre urls de classes:
# Consultar a documentação em: https://docs.djangoproject.com/pt-br/4.2/ref/class-based-views/generic-display/#listview

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('pagina/<slug:slug>/', PageDetailView.as_view(), name='page'), # type: ignore
    path(
        'page/<slug:slug>/',
        RedirectView.as_view(pattern_name='blog:page', permanent=True),
        name='page_legacy',
    ),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'), 
    path('created_by/<int:author_pk>/', CreatedByListView.as_view(), name='created_by'), 
    path('categoria/<slug:slug>/', CategoryListView.as_view(), name='category'), # type: ignore
    path(
        'category/<slug:slug>/',
        RedirectView.as_view(pattern_name='blog:category', permanent=True),
        name='category_legacy',
    ),
    path('tag/<slug:slug>/', TagListView.as_view(), name='tag'), # type: ignore
    path('serarch/', SearchListView.as_view(), name='search'), 

]
