from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path("", views.index, name="main"),
    path("admin/", admin.site.urls),
    path("about/", views.about, name="about"),
    path('mdeditor/', include('mdeditor.urls')),
    # Подключаем blog.urls
    path("blog/", include("blog.urls")),
]
