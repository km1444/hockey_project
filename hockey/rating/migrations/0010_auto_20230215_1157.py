# Generated by Django 2.2.19 on 2023-02-15 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0009_auto_20230205_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AddConstraint(
            model_name='player',
            constraint=models.UniqueConstraint(fields=('name', 'year_of_birth'), name='unique_player'),
        ),
    ]