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


## Lesson 56

### Как установить все зависимости из файла requirements.txt
```bash
pip install -r requirements.txt
```

Команда заглянет в файл requirements.txt и установит все зависимости, которые там указаны.

### Алгоритм запуска этого Django проекта

1. Склонировали проект себе на компьютер
2. Подняли виртуальное окружение
3. Выполнили команду `pip install -r requirements.txt` - установили все зависимости
4. Выполнили команду `python manage.py migrate` - создали таблицы в базе данных
5. Запустили сервер командой `python manage.py runserver`


Если есть желание экспериментировать с этим проектом, вы можете создать
отдельную ветку и вносить туда свои изменения.

Как только проект обновляется на гитхабе, вы можете скачать обновления. И даже слить их в вашу ветку для экспериментов, или создать новую ветку из главной, под новые эксперименты.


### Усложняем модель пользователя.

```python
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


class Post(models.Model):
    """
    Модель поста
    """
    title = models.CharField(max_length=200)
    text = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = models.JSONField(null=True, blank=True, default=list)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для автоматической генерации slug
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        """
        Строковое представление модели
        """
        return self.title

    def get_absolute_url(self):
        """
        Метод для получения абсолютного URL поста
        """
        return f'/post/{self.slug}/'
```

1. **Создайте и примените миграции:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Запуск shell_plus:**
   ```bash
   python manage.py shell_plus
   ```

3. **Добавьте посты через shell_plus:**
   ```python
   from your_app.models import Post
   from django.contrib.auth import get_user_model
   User = get_user_model()

   user = User.objects.create_user('testuser', password='password')


    Post.objects.create(title='Первый пост', text='Текст первого поста', author=user, tags=['первый', 'пост'])

    # Получим послднюю запись

    post = Post.objects.last()


На текущий момент не получится создать пост без пользователей в системе.
Т.е. надо сначала будет создать пользователя, а уже потом создавать пост.

Очень часто, первым создают суперпользователя, через команду:

```bash
python manage.py createsuperuser
```

У этого пользователя будут максимальные права в системе.

Добудем пользователя с username `admin`
Создадим пост от его имени

```python

user = User.objects.get(username='admin')

Post.objects.create(title='Второй пост', text='Текст второго поста', author=user, tags=['второй', 'пост'])

```

Есть проблема со слагификацицией кириллицы. Для того чтобы это исправить, надо установить библиотеку `unidecode`

```bash
pip install unidecode
```

Импортировать её в модели.

```python
from unidecode import unidecode

# Использовать в слагификации
self.slug = slugify(unidecode(self.title))
```

### Регистрация моделей в админке.

Базовую регистрацию можно сделать 2 способами:

1. **Создать файл `admin.py` в папке приложения и зарегистрировать модель:**
   ```python
   from django.contrib import admin
   from .models import Post

   admin.site.register(Post)
   ```

2. **Создать класс PostAdmin в файле `admin.py` и зарегистрировать модель:**
   ```python
   from django.contrib import admin
   from .models import Post

   @admin.register(Post)
   class PostAdmin(admin.ModelAdmin):
       list_display = ('title', 'author', 'published_date')
       list_filter = ('author', 'published_date')
       search_fields = ('title', 'text')
   ```


### Адаптация шаблонов для новой модели

В целом адаптация почти не понадобилась. Поля модели совпали с с ключами словарей, которые мы использовали ранее, для контекста.
Единственное, был поправлен get_absolute_url в модели, который вел на несуществующий адрес.

Коммит:
**models: запустили рендер постов из модели Post**


## CKEditor

Для того чтобы добавить CKEditor в ваше Django-приложение и использовать его только в админке для редактирования и добавления постов, выполните следующие шаги:

### 1. Установка необходимых библиотек

Используйте `pip` для установки `django-ckeditor`:

```sh
pip install django-ckeditor
```

### 2. Настройки Django

#### a. Добавьте `ckeditor` и `ckeditor_uploader` в `INSTALLED_APPS` в вашем `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'ckeditor',
    'ckeditor_uploader',
    ...
]
```

#### b. Настройте пути для загрузки файлов CKEditor:

Добавьте следующие строки в `settings.py`:

```python
CKEDITOR_UPLOAD_PATH = "uploads/"
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
```

Если этих папок нет, создайте их в корне проекта.

### 3. Конфигурация URL

#### a. В основном файле `urls.py` вашего проекта добавьте путь для CKEditor:

```python
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    ...
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Добавили в пути `ckeditor/` и подключили `ckeditor_uploader.urls` для загрузки файлов.
Конструкция `if settings.DEBUG:` добавляет путь к медиафайлам только в режиме отладки, в боевом режиме это будет делать веб-сервер.

