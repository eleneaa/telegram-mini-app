# Generated by Django 4.1.13 on 2025-04-28 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlases', '0005_atlas_tooltips'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atlas',
            name='tooltips',
            field=models.JSONField(default=dict, verbose_name='Координаты подсказок'),
        ),
    ]
