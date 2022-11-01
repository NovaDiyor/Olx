from django.contrib import admin
from django.urls import path, include
from api.router import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('api/', include('api.urls')),
    path('routers/', include(routers.urls)),
]
