# Generated by Django 2.2.16 on 2022-05-14 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0014_title_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
    ]