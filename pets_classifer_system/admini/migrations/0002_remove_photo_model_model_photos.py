# Generated by Django 4.0.4 on 2023-06-19 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admini', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='model',
        ),
        migrations.AddField(
            model_name='model',
            name='photos',
            field=models.ManyToManyField(to='admini.photo'),
        ),
    ]
