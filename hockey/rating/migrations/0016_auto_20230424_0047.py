# Generated by Django 2.2.16 on 2023-04-24 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0015_auto_20230415_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistic',
            name='season',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='rating.Season', verbose_name='Сезон'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='team',
            field=models.ForeignKey(blank=True, default=15, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='rating.Team', verbose_name='Команда'),
        ),
    ]