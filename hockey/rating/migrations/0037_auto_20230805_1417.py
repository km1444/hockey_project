# Generated by Django 2.2.16 on 2023-08-05 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0036_auto_20230729_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalkeeperStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.SmallIntegerField(default=14, verbose_name='Возраст')),
                ('game', models.SmallIntegerField(default=1, verbose_name='Игры')),
                ('goal_against', models.SmallIntegerField(default=0, verbose_name='Голы')),
                ('penalty', models.SmallIntegerField(default=0, verbose_name='Штраф')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goalkeeperstatistic', to='rating.Player', verbose_name='Игрок')),
                ('position', models.ForeignKey(blank=True, default=3, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goalkeeperstatistic', to='rating.Position', verbose_name='Позиция')),
                ('season', models.ForeignKey(default=22, on_delete=django.db.models.deletion.CASCADE, related_name='goalkeeperstatistic', to='rating.Season', verbose_name='Сезон')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goalkeeperstatistic', to='rating.Team', verbose_name='Команда')),
            ],
            options={
                'verbose_name': 'Статистик Вратаря',
                'verbose_name_plural': 'Статистика Вратарей',
                'ordering': ('game',),
            },
        ),
        migrations.DeleteModel(
            name='GolkeeperStatistic',
        ),
    ]