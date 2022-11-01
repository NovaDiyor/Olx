from django.urls import path
from .views import *

urlpatterns = [
    path('search_category/<int:pk>/', category_filter),
    path('search_subcategory/<int:pk>/', subcategory_filter),
    path('search_ads/<int:pk>/', ads_filter),
    path('search_region/', search_region),
    path('search_category/<int:pk>/', category_filter),
    path('profile/', profile),
    path('add_wishlist/', wishlist_add),
    path('another_profile/<int:pk>/', another_profile),

]
