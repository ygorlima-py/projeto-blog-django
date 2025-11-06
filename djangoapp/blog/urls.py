from django.urls import path
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
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page'), # type: ignore
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'), 
    path('created_by/<int:author_pk>/', CreatedByListView.as_view(), name='created_by'), 
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category'), # type: ignore
    path('tag/<slug:slug>/', TagListView.as_view(), name='tag'), # type: ignore
    path('serarch/', SearchListView.as_view(), name='search'), 

]
