# Generated by Django 2.2 on 2022-01-29 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.TextField(max_length=100, verbose_name='Заголовок'),
        ),
    ]
