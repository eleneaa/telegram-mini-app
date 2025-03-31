# Generated by Django 4.1.13 on 2024-11-13 11:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atlas',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=100, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=50, verbose_name='Название файла')),
                ('atlas_file', models.ImageField(upload_to='atlases_storage', verbose_name='Файл атласа')),
                ('catalogs', models.ManyToManyField(blank=True, related_name='atlases', to='categories.catalog', verbose_name='Принадлежит каталогам')),
            ],
            options={
                'verbose_name': 'Атлас',
                'verbose_name_plural': 'Атласы',
            },
        ),
    ]
