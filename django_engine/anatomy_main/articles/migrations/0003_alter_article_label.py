# Generated by Django 5.1.3 on 2025-01-12 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_article_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='label',
            field=models.CharField(max_length=200, verbose_name='Название файла'),
        ),
    ]
