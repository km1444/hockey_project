# Generated by Django 2.2.19 on 2023-01-09 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0006_auto_20230102_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistic',
            name='age',
            field=models.SmallIntegerField(default=14, verbose_name='Возраст'),
        ),
    ]
