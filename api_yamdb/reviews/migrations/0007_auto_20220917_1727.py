# Generated by Django 2.2.16 on 2022-09-17 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20220917_1722'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(help_text='Введите дату выпуска', verbose_name='Дата выпуска'),
        ),
    ]