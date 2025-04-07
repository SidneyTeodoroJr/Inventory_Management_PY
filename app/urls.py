from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('products.api_urls')),
    path('', admin.site.urls),
]
