# Generated by Django 3.2.23 on 2024-05-22 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liga2_seasons_app', '0006_alter_teamintable1gr_team_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transitiontournament',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]