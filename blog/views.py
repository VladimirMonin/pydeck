from django.shortcuts import render, HttpResponse

USERS_COUNT = 10


def about(request):
    context = {'users_count': USERS_COUNT}
    return render(request, "about.html")


def blog_catalog(request):
    return HttpResponse("<h1>Каталог постов</h1>")
