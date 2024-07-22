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

## Lesson 57
### Создали систему моделей близкую к конечной версии

```python

## Модели блога

Напишем близкие к конечному варианту модели.

### Модель категории

```python
from django.db import models
from django.utils.text import slugify
from typing import Any

class Category(models.Model):
    """
    Модель категории
    """
    name = models.CharField(max_length=200, unique=True) 
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs) -> None:
        """
        Переопределение метода save для автоматической генерации slug
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Строковое представление модели
        """
        return self.name

    # def get_absolute_url(self) -> str:
    #     """
    #     Заглушка для метода get_absolute_url
    #     """
    #     return f'/blog/category/{self.slug}/'


```

### Модель тега

```python
class Tag(models.Model):
    """
    Модель тега
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs) -> None:
        """
        Переопределение метода save для автоматического создания slug
        и приведения имени тега к нижнему регистру
        """
        if not self.slug:
            self.slug = slugify(self.name)
        self.name = self.name.lower().replace(' ', '_')
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Строковое представление модели
        """
        return self.name

    # def get_absolute_url(self) -> str:
    #     """
    #     Заглушка для метода get_absolute_url
    #     """
        
    #     return f'/tag/{self.slug}/'
```

### Модель комментария

```python
class Comment(models.Model):
    """
    Модель комментария
    """
    STATUS_CHOICES = [
        ('checked', 'Проверен'),
        ('unchecked', 'Не проверен'),
    ]

    # get_user_model() - функция, которая возвращает модель пользователя, используемую в проекте
    # on_delete=models.CASCADE - при удалении пользователя, удалять все его комментарии
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    # choices - список кортежей, в котором каждый кортеж содержит два элемента: значение и человекочитаемое имя
    # Мы сможем внести в это поле только одно из значений, указанных в STATUS_CHOICES
    # default='unchecked' - значение по умолчанию
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unchecked')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
```

### Модель поста

```python
from django.contrib.auth import get_user_model

class Post(models.Model):
    """
    Модель поста
    """
    title = models.CharField(max_length=200)
    text = models.TextField()
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # related_name - имя обратной связи. Это имя будет использоваться для обращения к связанным объектам
    # Например, если мы захотим получить все посты, связанные с тегом, мы можем использовать выражение tag.posts.all()
    tags = models.ManyToManyField('Tag', related_name='posts') 
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для автоматической генерации slug
        """
        if not self.slug or self.slug == '':
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)


    def __str__(self):
        """
        Строковое представление модели
        """
        return f'{self.title}: {self.slug}'

    def get_absolute_url(self):
        """
        Метод для получения абсолютного URL поста
        """
        return f'/blog/{self.slug}/'


```

Чтобы применить это в своем учебном проекте, вам нужно создать миграции и применить их:

```bash
python manage.py makemigrations
python manage.py migrate
```

После чего, вы получите новые таблицы в базе данных.

### Практика с моделями

1. **Запустите Django Shell Plus**

   ```bash
   python manage.py shell_plus
   ```

2. **Создайте категории**

   ```python
   # Создание категорий
   category1 = Category.objects.create(name='Программирование', slug='programmyrovanie')
   category2 = Category.objects.create(name='Веб-разработка', slug='web-razrabotka')
   category3 = Category.objects.create(name='Базы данных', slug='bazy_dannykh')
   ```

3. **Создайте теги**

   ```python
   # Создание тегов
   tag1 = Tag.objects.create(name='Python')
   tag2 = Tag.objects.create(name='Django')
   tag3 = Tag.objects.create(name='Flask')
   tag4 = Tag.objects.create(name='SQL', 
   tag5 = Tag.objects.create(name='SQLite', 
   tag6 = Tag.objects.create(name='PostgreSQL', 
   tag7 = Tag.objects.create(name='JavaScript', 
   tag8 = Tag.objects.create(name='HTML', 
   tag9 = Tag.objects.create(name='CSS', 
   tag10 = Tag.objects.create(name='Bootstrap 5')
   tag11 = Tag.objects.create(name='Верстка')
   tag12 = Tag.objects.create(name='Разработка web приложений')
   # TODO - Проблема со слагификатором даже с unidecode в теге 12 проигнорировал русские буквы вообще создав слаг web 
   ```

Добыть тег по имени

```python
tag = Tag.objects.get(name='Python')
all_tags = Tag.objects.all()

```

### Добавление постов

```python
# Автор - первая запись в таблице пользователей
user_model = get_user_model()
admin = user_model.objects.first()
# author = User.objects.get(username='admin')

post1 = Post.objects.create(
    title='Основы Python',
    text='Изучаем основы Python.',
    author=admin,
    category=category1
)
post1.tags.add(tag1.id, tag2.id, tag3.id)

post2 = Post.objects.create(
    title='Введение в Django',
    text='Начало работы с Django.',
    author=admin,
    category=category2
)

post2.tags.add(tag2.id)
```

Добудим тег поста 2 и потом все посты с этим тегом.

```python
post = Post.objects.get(title='Введение в Django')
tags = post.tags.all()
tag1 = tags[0]

posts = tag1.posts.all()
```

Запуск shell_plus с отображением SQL запросов

```bash
python manage.py shell_plus --print-sql
```