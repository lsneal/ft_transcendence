# Generated by Django 5.0.1 on 2024-02-08 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='player1',
            field=models.CharField(default='null', max_length=50),
        ),
        migrations.AddField(
            model_name='game',
            name='player2',
            field=models.CharField(default='null', max_length=50),
        ),
    ]
