# Generated by Django 5.0.4 on 2024-05-08 16:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dynamic_theme', '0016_theme_media_gallery'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mediagallery',
            options={'verbose_name': 'Media Gallery', 'verbose_name_plural': 'Media Galleries'},
        ),
        migrations.AlterField(
            model_name='theme',
            name='navbar',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='django_dynamic_theme.navbar'),
        ),
    ]