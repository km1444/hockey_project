# Generated by Django 3.2.23 on 2024-02-16 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0046_team_emblem'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='wikip',
            field=models.URLField(blank=True, verbose_name='Ссылка на википедию'),
        ),
    ]