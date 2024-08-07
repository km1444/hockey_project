# Generated by Django 2.2.16 on 2023-07-22 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0030_auto_20230718_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='golkeeperstatistic',
            name='season',
            field=models.ForeignKey(default=22, on_delete=django.db.models.deletion.CASCADE, related_name='golkeeperstatistic', to='rating.Season', verbose_name='Сезон'),
        ),
        migrations.AlterField(
            model_name='golkeeperstatistic',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='golkeeperstatistic', to='rating.Team', verbose_name='Команда'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='season',
            field=models.ForeignKey(default=22, on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='rating.Season', verbose_name='Сезон'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='team',
            field=models.ForeignKey(blank=True, default=11, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='rating.Team', verbose_name='Команда'),
        ),
    ]
