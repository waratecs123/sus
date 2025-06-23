from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),  # для новостей
    path('articles/', include('news.urls')),  # для статей
]