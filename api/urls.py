from django.urls import path
from .views import *

urlpatterns = [
    path('search-category/<int:pk>/', category_filter),
    path('search-subcategory/<int:pk>/', subcategory_filter),
    path('search-ads-by-subcategory/<int:pk>/', ads_filter),
    path('search/', search),
    path('search-category/<int:pk>/', category_filter),
    path('update-ads/', update_ads),
    path('delete-ads/', delete_ads),
    path('sale-ads/', sale_ads),
    path('profile/', profile),
    path('add-wishlist/', wishlist_add),
    path('another-profile/<int:pk>/', another_profile),
    path('register/', register),
    path('login/', login_view),
    path('reset-password/', reset_password),
    path('get-info/', get_info),
    path('statuses/', statuses),
    path('ads-page/', ads_page.as_view()),
    path('add-image/', add_ads_image),
    path('add-ads/', add_ads),
]
