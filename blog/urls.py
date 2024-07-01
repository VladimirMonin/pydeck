from django.contrib import admin
from django.urls import path
from .views import blog_catalog

urlpatterns = [
    path('', blog_catalog, name='blog_catalog'),

]
