# Generated by Django 4.1.13 on 2024-09-17 12:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=100, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=50, verbose_name='Описание вопроса')),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=100, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=50, verbose_name='Название теста')),
                ('catalogs', models.ManyToManyField(blank=True, related_name='tests', to='categories.catalog', verbose_name='Принадлежит каталогам')),
                ('questions_list', models.ManyToManyField(to='tests.question', verbose_name='Список вопросов')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='correct_variants',
            field=models.ManyToManyField(related_name='correct_variants', to='tests.variant', verbose_name='Список правильных ответов'),
        ),
        migrations.AddField(
            model_name='question',
            name='variants',
            field=models.ManyToManyField(related_name='variants', to='tests.variant', verbose_name='Список ответов'),
        ),
    ]
