from django.shortcuts import render
from django.http import HttpRequest
from .models import Post
from django.shortcuts import get_object_or_404
from django.db.models import F, Prefetch


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

        # Просто но не оптимально
        # posts = Post.objects.all()
        
        # prefetch_related - позволяет сделать запрос к связанным объектам
        # perfetch_relates - используется для многих ко многим и многих к одному
        posts = Post.objects.prefetch_related("tags", "category").all()
        # select_related - позволяет сделать запрос к связанным объектам
        # select_related - используется для одного к одному и одного ко многим
        # posts = Post.objects.select_related("category").all()

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
        "page_alias": "main",
    }
    return render(request, "index.html", context)


def post_detail(request, slug):
    # post: Post = get_object_or_404(Post, slug=slug)

    # prefetch_related - позволяет сделать запрос к связанным объектам

    post = Post.objects.prefetch_related("tags", "category").get(slug=slug)

    context = {
        "menu": menu,
        "post": post,
        "page_alias": "blog_catalog",
    }
    
    # Проверяем, есть ли в сессии информация о просмотренных постах
    if 'viewed_posts' not in request.session:
        request.session['viewed_posts'] = ['osnovy-python', 'osnovy-django', 'osnovy-django-2']
    
    # Если пост еще не был просмотрен, увеличиваем количество просмотров
    
    if slug not in request.session['viewed_posts']:
        post.views = F('views') + 1
        post.save(update_fields=['views'])
        request.session['viewed_posts'].append(slug)  # Добавляем пост в список просмотренных
        request.session.modified = True  # Указываем, что сессия была изменена для сохранения изменений
    
    # Отображаем пост
    return render(request, 'blog/post_detail.html', context)


def category_detail(request: HttpRequest, slug: str):
    """
    Функция - представление для страницы категории
    Принимает объект запроса HttpRequest и slug категории
    Отображает список статей с соответствующим slug

    Как это было бы на SQL

    SELECT * FROM post WHERE category_id = (
        SELECT id FROM category WHERE slug = slug
    )
    """
    posts = posts = Post.objects.filter(category__slug=slug)
    context = {
        "menu": menu,
        "posts": posts,
        "page_alias": "blog_catalog",
    }

    return render(request, "blog/blog_catalog.html", context)


def tag_detail(request: HttpRequest, slug: str):
    """
    Функция - представление для страницы тега
    Принимает объект запроса HttpRequest и slug тега
    Отображает список статей с соответствующим slug

    Как это было бы на SQL (многие ко многим)

    SELECT * FROM post WHERE id IN (
        SELECT post_id FROM post_tags WHERE tag_id = (
            SELECT id FROM tag WHERE slug = slug
        )
    )
    """
    posts = Post.objects.filter(tags__slug=slug)
    context = {
        "menu": menu,
        "posts": posts,
        "page_alias": "blog_catalog",
    }

    return render(request, "blog/blog_catalog.html", context)