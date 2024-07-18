from django.contrib import admin
from .models import Post
from mdeditor.widgets import MDEditorWidget
from django.db import models

class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget},
    }

admin.site.register(Post, PostAdmin)
