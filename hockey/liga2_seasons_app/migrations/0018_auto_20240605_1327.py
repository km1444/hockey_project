# Generated by Django 3.2.23 on 2024-06-05 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('liga2_seasons_app', '0017_transitionwithoutpoints'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transitionwithoutpoints',
            options={'verbose_name': 'Команда переходного турнира без ранее набранных очков', 'verbose_name_plural': 'Команды переходного турнира без ранее набранных очков'},
        ),
        migrations.AlterField(
            model_name='teamintable1gr',
            name='transition_tournament',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='liga2_seasons_app.transitiontournament', verbose_name='Участие в переходном турнире'),
        ),
        migrations.AlterField(
            model_name='teamintable2gr',
            name='transition_tournament',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='liga2_seasons_app.transitiontournament', verbose_name='Участие в переходном турнире'),
        ),
    ]
