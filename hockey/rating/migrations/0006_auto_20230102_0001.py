# Generated by Django 2.2.19 on 2023-01-01 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0005_auto_20221229_2347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statistic',
            options={'ordering': ('-point', 'game'), 'verbose_name': 'Статистика', 'verbose_name_plural': 'Статистика'},
        ),
        migrations.AlterField(
            model_name='statistic',
            name='assist',
            field=models.SmallIntegerField(default=0, verbose_name='Передачи'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='game',
            field=models.SmallIntegerField(default=1, verbose_name='Игры'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='goal',
            field=models.SmallIntegerField(default=0, verbose_name='Голы'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='penalty',
            field=models.SmallIntegerField(default=0, verbose_name='Штраф'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='point',
            field=models.SmallIntegerField(default=0, verbose_name='Очки'),
        ),
    ]