# Generated by Django 2.2.16 on 2022-05-13 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yamdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='year',
            field=models.IntegerField(verbose_name='Дата добавления'),
        ),
    ]