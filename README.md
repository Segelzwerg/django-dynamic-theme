![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-dynamic-theme)


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
static_url = "static/"
static_root = "static"
STATICFILES_FINDERS = [
    ...,
    "compressor.finders.CompressorFinder",
]
COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)
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
  <link type="text/x-scss" rel="stylesheet" href="{% static 'theme.scss' %}" />
  ...
</html>
```

3. Visit `http://127.0.0.1:8000/admin/django_dynamic_theme/` to start customizing your theme.
