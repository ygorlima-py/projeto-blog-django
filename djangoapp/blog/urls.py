from django.urls import path
from blog.views import (
                        PostListView, 
                        page, 
                        post, 
                        CreatedByListView, 
                        category, 
                        tag, 
                        search
                        )


# Para mais detalhes sobre urls de classes:
# Consultar a documentação em: https://docs.djangoproject.com/pt-br/4.2/ref/class-based-views/generic-display/#listview

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('page/<slug:slug>/', page, name='page'), # type: ignore
    path('post/<slug:slug>/', post, name='post'), 
    path('created_by/<int:author_pk>/', CreatedByListView.as_view(), name='created_by'), 
    path('category/<slug:slug>/', category, name='category'), # type: ignore
    path('tag/<slug:slug>/', tag, name='tag'), # type: ignore
    path('serarch/', search, name='search'), 

]
