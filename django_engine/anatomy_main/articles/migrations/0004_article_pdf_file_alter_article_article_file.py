# Generated by Django 5.0.9 on 2025-04-01 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_alter_article_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='pdf_file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='articles_storage', verbose_name='PDF-файл статьи'),
        ),
        migrations.AlterField(
            model_name='article',
            name='article_file',
            field=models.FileField(blank=True, null=True, upload_to='articles_storage', verbose_name='Файл статьи'),
        ),
    ]
