from django.urls import path

from .views import AffiliateListView


app_name = 'affiliates'

urlpatterns = [
    path('', AffiliateListView.as_view(), name='list'),
    path(
        'categoria/<slug:category_slug>/',
        AffiliateListView.as_view(),
        name='category',
    ),
]
