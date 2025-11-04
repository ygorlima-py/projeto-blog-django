from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post

POSTS_PER_PAGE = 9 

# Create your views here.
def index(request):
    posts = Post.objects.get_published() # type: ignore


    print(posts)

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(  
        request,
        'blog/pages/index.html',
        context= {
            'page_obj': page_obj,
        }
    )

def post(request, slug):

    post = Post.objects.get_published().filter(slug=slug).first() # type: ignore

    return render(
        request,
        'blog/pages/post.html',

        context={
            'post': post,
        }
    )

def created_by(request, author_pk):
    posts = Post.objects.get_published().filter(created_by__pk=author_pk) # type: ignore


    print(posts)

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(  
        request,
        'blog/pages/index.html',
        context= {
            'page_obj': page_obj,
        }
    )

def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug) # type: ignore
    
    print(posts)

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(  
        request,
        'blog/pages/index.html',
        context= {
            'page_obj': page_obj,
        }
    )

def page(request):

    return render(
        request,
        'blog/pages/page.html',
        context={
            # 'page_obj': page_obj,
        }
    )