# Generated by Django 5.0.3 on 2024-03-23 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_gamer_nb_game_alter_gamer_victory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamer',
            name='nb_game',
            field=models.IntegerField(default=150),
        ),
        migrations.AlterField(
            model_name='gamer',
            name='victory',
            field=models.IntegerField(default=15),
        ),
    ]