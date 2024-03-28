INSTALLED_APPS = [
    "compressor",
]
STATIC_URL = "static/"
STATIC_ROOT = "static"
STATICFILES_FINDERS = [
    "compressor.finders.CompressorFinder",
]
# Bootstrap Settings
COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)
BOOSTRAP5 = {
    "theme_url": "static/theme.css",
}
