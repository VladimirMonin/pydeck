from django.contrib import admin
from django.urls import path, include
from blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="main"),
    path("admin/", admin.site.urls),
    path("about/", views.about, name="about"),
    # Подключаем blog.urls
    path("blog/", include("blog.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),