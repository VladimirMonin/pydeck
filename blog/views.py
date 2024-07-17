from django.shortcuts import render
from django.http import HttpRequest
from .models import Post
from django.shortcuts import get_object_or_404

USERS_COUNT = 10


menu = [
    {"name": "Главная", "alias": "main"},
    {"name": "Блог", "alias": "blog_catalog"},
    {"name": "О проекте", "alias": "about"},
]


def about(request):
    """
    Вьюшка для страницы "О проекте"
    """
    context = {
        "users_count": USERS_COUNT,
        "menu": menu,
        "page_alias": "about",
    }


    return render(request, "about.html", context)


def blog_catalog(request):
    """
    Вьюшка для страницы "Блог" с каталогом постов.
    Обрабатываем поисковую форму, которая обрабатывается методом GET
    И пробуем получить от туда ключи:
        search
        searchInTitle
        searchInText
        searchInTags
    """
    
    if request.method == "GET":

        posts = Post.objects.all()
        
        context = {
            "menu": menu,
            "posts": posts,
            "page_alias": "blog_catalog",
        }
        return render(request, "blog/blog_catalog.html", context)


def index(request: HttpRequest):
    """
    Функция - представление для главной страницы
    Принимает объект запроса HttpRequest
    Вносит контекст дополнительные данные.
    """

    context = {
        "users_count": USERS_COUNT,
        "menu": menu,
        "posts": posts,
        "page_alias": "main",
    }
    return render(request, "index.html", context)


def post_detail(request: HttpRequest, slug: str):
    """
    Функция - представление для отдельной статьи
    Принимает объект запроса HttpRequest и slug статьи
    Отображает статью с соответствующим slug
    """
#    post = Post.objects.get(slug=slug)
    # post = Post.objects.filter(slug=slug).first()
    # get_object_or_404- метод, который возвращает объект или 404
    post: Post = get_object_or_404(Post, slug=slug)

    context = {
        "menu": menu,
        "post": post,
        "page_alias": "blog_catalog",
    }
    return render(request, "blog/post_detail.html", context)
