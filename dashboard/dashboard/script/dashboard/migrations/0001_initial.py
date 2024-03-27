# Generated by Django 5.0.3 on 2024-03-27 08:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gamer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pseudo', models.CharField(max_length=50)),
                ('victory', models.IntegerField(default=0)),
                ('nb_game', models.IntegerField(default=0)),
                ('nb_tournament', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conceded_point', models.IntegerField(default=0)),
                ('marked_point', models.IntegerField(default=0)),
                ('opponent', models.CharField(default='', max_length=50)),
                ('gamer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.gamer')),
            ],
        ),
    ]
