from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("about/", views.about),
    # Подключаем blog.urls
    path("blog/", include("blog.urls")),
]
