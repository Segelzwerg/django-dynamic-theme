![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-dynamic-theme)


[![codecov](https://codecov.io/gh/Segelzwerg/django-dynamic-theme/graph/badge.svg?token=YBTYAESSWE)](https://codecov.io/gh/Segelzwerg/django-dynamic-theme)

# Django Dynamic Theme
This allows an administrator of a django website to change the theme on the fly.

## Installation

```sh
pip install django-dynamic-theme
```

## Quickstart

1. Add `django-dynamic-theme` to your INSTALLED_APPS:

```python
INSTALLED_APPS = [
  ...,
  "django_dynamic_theme",
]
```

2. Run `python manage.py migrate`

3. Visit `http://127.0.0.1:8000/admin/django_dynamic_theme/` to start customizing your theme.
