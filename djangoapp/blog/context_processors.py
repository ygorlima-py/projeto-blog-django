from blog.models import Category


def navigation_categories(request):
    categories = (
        Category.objects
        .filter(post__is_published=True)
        .distinct()
        .order_by('name')
    )

    return {
        'navigation_categories': categories,
    }
