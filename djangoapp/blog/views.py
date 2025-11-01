from django.shortcuts import render

# Create your views here.
def index(request):
    return render(
        request,
        'blog/pages/index.html',
        context={
            'nome': 'Ygor Lima'
        }
    )

def post(request):
    return render(
        request,
        'blog/pages/post.html',
        context={
            'nome': 'Ygor Lima'
        }
    )

def page(request):
    return render(
        request,
        'blog/pages/page.html',
        context={
            'nome': 'Ygor Lima'
        }
    )