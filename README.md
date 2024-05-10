![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-dynamic-theme)
[![](https://img.shields.io/pypi/djversions/django-dynamic-theme?color=0C4B33&logo=django&logoColor=white&label=django)](https://www.djangoproject.com/)
![GitHub Release](https://img.shields.io/github/v/release/segelzwerg/django-dynamic-theme)


[![Documentation Status](https://readthedocs.org/projects/django-dynamic-theme/badge/?version=latest)](https://django-dynamic-theme.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/Segelzwerg/django-dynamic-theme/graph/badge.svg?token=YBTYAESSWE)](https://codecov.io/gh/Segelzwerg/django-dynamic-theme)

# Django Dynamic Theme
This allows an administrator of a django website to change the theme on the fly.

## Installation

```sh
pip install django-dynamic-theme
```

## Quickstart

1. Add  the following settings::

```python
INSTALLED_APPS = [
  ...,
  "django_dynamic_theme",
  "compressor",
]
...
# Default setting but you can set it to some other path.
STATIC_URL = "static/"
STATIC_ROOT = "static"
STATICFILES_FINDERS = [
    ...,
    "compressor.finders.CompressorFinder",
]
COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)
MIDDLEWARE = [
    ...,
    "django_dynamic_theme.middleware.MissingThemeHandleMiddleware",
]
TEMPLATES = {
  "OPTIONS": {
    "context_processors": [
      ...,
      "django_dynamic_theme-context_processor.theme",
    ]
  }
}
```
2. Run `python manage.py migrate`

3. Assuming you have `base.html` add this to it before the `<body>` tag:
```html
<html>
  ...
  {% load compress %}
  {% load static %}
  {% compress css %}
  <link type="text/x-scss" rel="stylesheet" href="{% static theme_file %}" />
  ...
</html>
```

3. Visit `http://127.0.0.1:8000/admin/django_dynamic_theme/` to start customizing your theme.
