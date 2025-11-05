from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic.list import ListView
'''
Views de exibição genéricas

É uma lista? ou em um único objeto só?

Se for lista  use ListView
Se for um único objeto só use DetailView

Para mais detalhes consulte: https://docs.djangoproject.com/pt-br/4.2/ref/class-based-views
'''

POSTS_PER_PAGE = 1 

class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html' 
    context_object_name = 'posts'
    ordering = '-pk',
    paginate_by = POSTS_PER_PAGE
    queryset = Post.objects.get_published() #type: ignore

    # def get_queryset(self):

    #     queryset = super().get_queryset()
    #     print('antes: ', queryset)

    #     queryset = queryset.filter(is_published=True)
    #     print('depois: ', queryset)

    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'home - ' 
        })
        return context


# def index(request):
#     posts = Post.objects.get_published() # type: ignore


#     print(posts)

#     paginator = Paginator(posts, POSTS_PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(  
#         request,
#         'blog/pages/index.html',
#         context= {
#             'page_obj': page_obj,
#             'page_title': 'Home - ',
#         }
#     )

def post(request, slug):

    post_obj = Post.objects.get_published().filter(slug=slug).first() # type: ignore

    return render(
        request,
        'blog/pages/post.html',

        context={
            'post': post_obj,
            'page_title': post_obj.title
        }
    )

def created_by(request, author_pk):
    user = User.objects.filter(pk=author_pk).first()

    if user is None:
        raise Http404()
    
    posts = Post.objects.get_published().filter(created_by__pk=author_pk) # type: ignore

    user_full_name = user.username 

    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name}'

    page_title = f'Posts de {user_full_name} - '

    print(posts)

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(  
        request,
        'blog/pages/index.html',
        context= {
            'page_obj': page_obj,
            'page_title': page_title,

        }
    )

def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug) # type: ignore
    
    print(posts)

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404
    
    page_title = f'{page_obj[0].category.name} - Categoria - '

    return render(  
        request,
        'blog/pages/index.html',
        context= {
            'page_obj': page_obj,
            'page_title': page_title,

        }
    )

def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug=slug) # type: ignore
    

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404
    
    page_title = f'{page_obj[0].tags.first().name} - Tag - '


    return render(  
        request,
        'blog/pages/index.html',
        context= {
            'page_obj': page_obj,
            'page_title': page_title,

        }
    )

def search(request):
    search_value = request.GET.get('search', '').strip()
    
    posts = ( 
        Post.objects.get_published() # type: ignore
        .filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value) 
            ) [:POSTS_PER_PAGE]
    )
    
    page_title = f'{search_value[:30]} - search'

    return render(  
        request,
        'blog/pages/index.html',
        context= {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,

        }
    )

def page(request, slug):

    page_obj = Page.objects.filter(is_published=True).filter(slug=slug).first() # type: ignore
    
    if page_obj is None:
        raise Http404()
    
    page_title = f'{page_obj.title} - '
    return render(
        request,
        'blog/pages/page.html',
        context={
            'page': page_obj,
            'page_title': page_title,

        }
    )