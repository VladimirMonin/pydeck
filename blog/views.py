from django.shortcuts import render, HttpResponse

USERS_COUNT = 10

def about(request):
    return HttpResponse(f'<h1>О блоге</h1><p>Пользователей: {USERS_COUNT}</p>')
