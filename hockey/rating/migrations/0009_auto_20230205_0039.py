# Generated by Django 2.2.19 on 2023-02-04 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0008_auto_20230205_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.TextField(unique=True, verbose_name='Текст'),
        ),
    ]
