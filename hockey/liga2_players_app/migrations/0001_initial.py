# Generated by Django 3.2.23 on 2024-06-13 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rating', '0056_auto_20240327_2318'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticPlayers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.SmallIntegerField(default=14, verbose_name='Возраст')),
                ('game', models.SmallIntegerField(default=1, verbose_name='Игры')),
                ('goal', models.SmallIntegerField(default=0, verbose_name='Голы')),
                ('assist', models.SmallIntegerField(default=0, verbose_name='Передачи')),
                ('point', models.SmallIntegerField(default=0, verbose_name='Очки')),
                ('penalty', models.SmallIntegerField(default=0, verbose_name='Штраф')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics_player', to='rating.player', verbose_name='Игрок')),
                ('position', models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='statistics_player', to='rating.position', verbose_name='Позиция')),
                ('season', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='statistics_player', to='rating.season', verbose_name='Сезон')),
                ('team', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='statistics_player', to='rating.team', verbose_name='Команда')),
            ],
            options={
                'verbose_name': 'Статистика полевого игрока',
                'verbose_name_plural': 'Статистика полевых игроков',
                'ordering': ('-season',),
            },
        ),
        migrations.AddConstraint(
            model_name='statisticplayers',
            constraint=models.UniqueConstraint(fields=('name', 'team', 'season'), name='unique_statistic_players'),
        ),
    ]