
# KitStock

KitStock is a Django app to conduct Web-based kitstock. For each question,
visitors can choose between a fixed number of answers.
Detailed documentation is in the "docs" directory.

## Quick start

- Add "kitstock" to your INSTALLED_APPS setting like this::
```python
INSTALLED_APPS = [
    ...
    'django.handkit.kitstock',
]
```

- Include the polls URLconf in your project urls.py like this::
```python
    url(r'^kitstock/', include('django.handkit.kitstock')
```

- Run ``python manage.py migrate`` to create the kitstock models.

- Start the development server and visit：
```python
    http://127.0.0.1:8000/admin/
```

- Build kitstock package:
```python
    python setup.py sdist
```
This creates a directory called dist and builds your new package, django-polls-0.1.tar.gz.

- Install or uninstall kitstock package
```python
install：
    pip install dist/django-handkit-kitstock-0.1.tar.gz

uninstall：
    pip uninstall django-handkit-kitstock
```

