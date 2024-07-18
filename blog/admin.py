from django.contrib import admin
from .models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

admin.site.register(Post, PostAdmin)
