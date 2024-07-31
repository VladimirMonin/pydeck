from django.contrib import admin
from django.urls import path
from .views import blog_catalog, post_detail, category_detail, tag_list

urlpatterns = [
    path('', blog_catalog, name='blog_catalog'),
    # Маршрут с конвертером slug для отображения отдельной статьи
    # /blog/osnovy_python/
    path('<slug:slug>/', post_detail, name='post_detail'),
    path('category/<slug:slug>/', category_detail, name='category_detail'),
    path('tag/<slug:slug>/', tag_list, name='tag_list'),
    
]
