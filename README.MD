## Django



Команда создания Django проекта
```bash
django-admin startproject <project_name> .
```

Команда создания Django приложения

```bash
python manage.py startapp <app_name> 
```

Подключение `templates` из корня проекта в `settings.py`
```python
TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
    },
]
```

## Команды миграций

Эта команда создаст файлы миграций, которые описывают изменения в БД, которые необходимо применить. 

Создание миграции
```bash
python manage.py makemigrations
```

Эта команда применит миграции к БД

Применение миграции
```bash
python manage.py migrate
```

## Установили Shell plus

```bash
pip install django-extensions
```

Добавили в `INSTALLED_APPS` в `settings.py`
```python
INSTALLED_APPS = [
    ...
    'django_extensions',
    ...
]
```

## Команды Shell plus


```python
# Импортируем модель Post
from blog.models import Post

# Добавляем записи
Post.objects.create(title='Первый пост', text='Текст первого поста')
Post.objects.create(title='Второй пост', text='Текст второго поста')
Post.objects.create(title='Третий пост', text='Текст третьего поста')
Post.objects.create(title='Четвертый пост', text='Текст четвертого поста')
Post.objects.create(title='Пятый пост', text='Текст пятого поста')
```

```python
# Получение всех записей
all_posts = Post.objects.all()

# Фильтрация записей
filtered_posts = Post.objects.filter(title__contains='пост')

# Получение одной записи по условию
single_post = Post.objects.get(id=1)
```