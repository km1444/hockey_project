# Generated by Django 2.2.16 on 2023-07-16 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0027_auto_20230716_1255'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonRound2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rating.TeamForTable2Round', verbose_name='')),
            ],
        ),
        migrations.AlterField(
            model_name='teamfortable',
            name='round_2',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables', to='rating.PersonRound2'),
        ),
    ]