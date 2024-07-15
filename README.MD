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
