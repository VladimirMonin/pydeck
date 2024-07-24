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

## Lesson 58 - Практика с ORM

### Упражнения для практики с менеджером объектов в Django с решениями

#### Добавление категорий, тегов и пользователей

1. **Запустите Django Shell Plus**

   ```bash
   python manage.py shell_plus --print-sql
   ```
Команда `python manage.py shell_plus --print-sql` запускает интерактивную оболочку Django (shell_plus) и позволяет выводить SQL-запросы, которые выполняются в процессе работы с объектами моделей. Это полезно для отладки и анализа того, какие именно запросы формируются при взаимодействии с базой данных.

2. **Создайте категории**

   ```python
   # Создание категорий
   category1 = Category.objects.create(name='Программирование')
   category2 = Category.objects.create(name='Веб-разработка')
   category3 = Category.objects.create(name='Базы данных')
   ```

3. **Создайте теги**

   ```python
   # Создание тегов
   tag1 = Tag.objects.create(name='Python')
   tag2 = Tag.objects.create(name='Django')
   tag3 = Tag.objects.create(name='Flask')
   tag4 = Tag.objects.create(name='SQL')
   tag5 = Tag.objects.create(name='SQLite')
   tag6 = Tag.objects.create(name='PostgreSQL')
   tag7 = Tag.objects.create(name='JavaScript')
   tag8 = Tag.objects.create(name='HTML')
   tag9 = Tag.objects.create(name='CSS')
   tag10 = Tag.objects.create(name='Bootstrap 5')
   ```

Для добавления нескольких объектов в Django с помощью одного запроса в `shell_plus`, вы можете использовать метод `bulk_create`. Это позволит вам создать все эти теги за один запрос к базе данных. Вот как это можно сделать:


Этот код создаст список объектов `Tag`, а затем выполнит их добавление в базу данных за один запрос, что значительно эффективнее, чем создание каждого объекта по отдельности.

4. **Создайте пользователей**

```python
from django.contrib.auth import get_user_model

User = get_user_model()
user1 = User.objects.create_user(username='user1', password='password1')
user2 = User.objects.create_user(username='user2', password='password2')
```

#### Добавление постов для каждого пользователя

##### Простой способ через ID тегов и категорий

1. **Добавьте посты для пользователя user1**

```python
# Посты для user1
   post1 = Post.objects.create(
	   title='Основы Python',
	   text='Изучаем основы Python.',
	   author=user1,
	   category=category1
   )
post1.tags.add(tag1.id, tag2.id)

post2 = Post.objects.create(
   title='Введение в Django',
   text='Начало работы с Django.',
   author=user1,
   category=category2
)
post2.tags.add(tag2.id, tag8.id)

post3 = Post.objects.create(
   title='Работа с базами данных',
   text='Как работать с базами данных в Python.',
   author=user1,
   category=category3
)
post3.tags.add(tag4.id, tag5.id)
```

##### Добавление постов через объекты тегов и категорий

2. **Добавьте посты для пользователя user2**

   ```python
   # Посты для user2
   post4 = Post.objects.create(
       title='Изучаем Flask',
       text='Основы Flask.',
       author=user2,
       category=category1
   )
   post4.tags.add(tag3, tag7)

   post5 = Post.objects.create(
       title='HTML и CSS',
       text='Создание веб-страниц с использованием HTML и CSS.',
       author=user2,
       category=category2
   )
   post5.tags.add(tag8, tag9)

   post6 = Post.objects.create(
       title='Работа с PostgreSQL',
       text='Настройка и использование PostgreSQL.',
       author=user2,
       category=category3
   )
   post6.tags.add(tag6)
   ```

#### Выполнение дополнительных операций

1. **Получите все комментарии одного пользователя**

   ```python
   comments_user1 = Comment.objects.filter(author='Иван Иванов')
   ```

2. **Подсчитайте количество комментариев пользователя**

   ```python
   count_comments_user1 = comments_user1.count()
   ```

3. **Найдите все теги всех постов, под которыми пользователь оставил комментарии**

   ```python
   posts_with_comments_user1 = Post.objects.filter(comments__author='Иван Иванов').distinct()
   tags_with_comments_user1 = Tag.objects.filter(post__in=posts_with_comments_user1).distinct()
   ```

### Упражнения для практики с менеджером объектов в Django

1. **Получить первый пост пользователя `user1`**
   Этот запрос возвращает самый первый пост пользователя `user1`, используя метод `first()`, который возвращает первый объект в наборе данных.

   ```python
   first_post_user1 = Post.objects.filter(author=user1).first()
   print(first_post_user1)
   ```

2. **Получить все посты пользователя `user1`**
   Этот запрос возвращает все посты, которые были созданы пользователем `user1`. Результат будет представлен в виде QuerySet.

   ```python
   all_posts_user1 = Post.objects.filter(author=user1)
   for post in all_posts_user1:
       print(post)
   ```

3. **Получить все посты пользователя `user1` в обратном порядке**
   Этот запрос возвращает все посты пользователя `user1`, отсортированные в обратном порядке по дате публикации, начиная с самых новых.

   ```python
   all_posts_user1_desc = Post.objects.filter(author=user1).order_by('-published_date')
   for post in all_posts_user1_desc:
       print(post)
   ```

4. **Получить все посты по тегу `Django`**
   Этот запрос возвращает все посты, которые имеют тег `Django`. Связь между постами и тегами осуществляется через поле `tags`.

   ```python
   django_posts = Post.objects.filter(tags__name='Django')
   for post in django_posts:
       print(post)
   ```

5. **Получить все теги поста `post1`**
   Этот запрос возвращает все теги, связанные с постом `post1`. Связь осуществляется через поле `tags` модели `Post`.

   ```python
   post1_tags = post1.tags.all()
   for tag in post1_tags:
       print(tag)
   ```

6. **Получить все посты, отсортированные по заголовку**
   Этот запрос возвращает все посты, отсортированные по заголовку в алфавитном порядке. Метод `order_by` используется для сортировки.

   ```python
   posts_sorted_by_title = Post.objects.all().order_by('title')
   for post in posts_sorted_by_title:
       print(post)
   ```

7. **Получить все посты, содержащие в заголовке слово "работа"**
   Этот запрос возвращает все посты, заголовки которых содержат слово "работа". Метод `filter` с использованием `icontains` обеспечивает поиск без учета регистра.

   ```python
   posts_with_work = Post.objects.filter(title__icontains='работа')
   for post in posts_with_work:
       print(post)
   ```

8. **Получить все посты, опубликованные в категории `category2`**
   Этот запрос возвращает все посты, которые были опубликованы в категории `category2`. Используется поле `category` модели `Post` для фильтрации.

   ```python
   category2_posts = Post.objects.filter(category=category2)
   for post in category2_posts:
       print(post)
   ```

9. **Получить все посты, не имеющие тегов**
   Этот запрос возвращает все посты, которые не имеют связанных тегов. Используется метод `filter` с условием `isnull=True`.

   ```python
   posts_without_tags = Post.objects.filter(tags__isnull=True)
   for post in posts_without_tags:
       print(post)
   ```

10. **Получить все посты, у которых более одного тега**
    Этот запрос возвращает все посты, у которых более одного тега. Используется метод `annotate` для подсчета тегов и `filter` для применения условия.

    ```python
    posts_with_multiple_tags = Post.objects.annotate(num_tags=models.Count('tags')).filter(num_tags__gt=1)
    for post in posts_with_multiple_tags:
        print(post)
    ```

11. **Получить все посты, созданные за последнюю неделю**
    Этот запрос возвращает все посты, которые были созданы за последние 7 дней. Используется текущее время и `timedelta` для вычисления границы времени.

    ```python
    from django.utils import timezone
    from datetime import timedelta

    last_week = timezone.now() - timedelta(days=7)
    recent_posts = Post.objects.filter(published_date__gte=last_week)
    for post in recent_posts:
        print(post)
    ```

12. **Получить все посты, у которых категория задана**
    Этот запрос возвращает все посты, у которых задана категория. Используется метод `filter` с условием `isnull=False`.

    ```python
    posts_with_category = Post.objects.filter(category__isnull=False)
    for post in posts_with_category:
        print(post)
    ```

13. **Получить количество постов для каждой категории**
    Этот запрос возвращает количество постов для каждой категории. Используется метод `annotate` для подсчета постов в каждой категории.

    ```python
    from django.db.models import Count

    category_post_counts = Category.objects.annotate(num_posts=Count('posts'))
    for category in category_post_counts:
        print(f'{category.name}: {category.num_posts}')
    ```

14. **Получить количество постов для каждого тега**
    Этот запрос возвращает количество постов для каждого тега. Используется метод `annotate` для подсчета постов, связанных с каждым тегом.

    ```python
    tag_post_counts = Tag.objects.annotate(num_posts=Count('posts'))
    for tag in tag_post_counts:
        print(f'{tag.name}: {tag.num_posts}')
    ```

15. **Получить все теги, отсортированные по количеству постов**
    Этот запрос возвращает все теги, отсортированные по количеству постов в порядке убывания. Используется метод `annotate` для подсчета и `order_by` для сортировки.

    ```python
    tags_sorted_by_posts = Tag.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')
    for tag in tags_sorted_by_posts:
        print(tag)
    ```

16. **Получить все посты, автор которых `user2` и у которых более двух тегов**
    Этот запрос возвращает все посты, автором которых является `user2` и у которых более двух тегов. Используется метод `annotate` и фильтр по количеству тегов.

    ```python
    user2_posts_with_multiple_tags = Post.objects.filter(author=user2).annotate(num_tags=Count('tags')).filter(num_tags__gt=2)
    for post in user2_posts_with_multiple_tags:
        print(post)
    ```

17. **Получить все посты, отсортированные по дате публикации в порядке убывания**
    Этот запрос возвращает все посты, отсортированные по дате публикации в порядке убывания. Используется метод `order_by` с параметром `-published_date`.

    ```python
    posts_sorted_by_date_desc = Post.objects.all().order_by('-published_date')
    for post in posts_sorted_by_date_desc:
        print(post)
    ```

18. **Получить все посты, опубликованные в категории `category1` и содержащие тег `Python`**
    Этот запрос возвращает все посты, которые были опубликованы в категории `category1` и содержат тег `Python`. Используется метод `filter` с несколькими условиями.

    ```python
    category1_python_posts = Post.objects.filter(category=category1, tags__name='Python')
    for post in category1_python_posts:
        print(post)
    ```

19. **Получить все посты, опубликованные после определенной даты**
    Этот запрос возвращает все посты, которые были опубликованы после определенной даты. Используется метод `filter` с условием по дате публикации.

    ```python
    from django.utils import timezone

    specific_date = timezone.datetime(2023, 1, 1)
    posts_after_specific_date = Post.objects.filter(published_date__gt=specific_date)
    for post in posts_after_specific_date:
        print(post)
    ```

20. **Получить все категории, в которых есть хотя бы один пост**
    Этот запрос возвращает все категории, в которых есть хотя бы один пост. Используется метод `filter` с условием по связанным постам и `distinct` для исключения дублирующих записей.

    ```python
    categories_with_posts = Category.objects.filter(posts__isnull=False).distinct()
    for category in categories_with_posts:
        print(category)
    ```
