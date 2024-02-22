# Generated by Django 5.0.2 on 2024-02-16 15:03

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_usergame'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nb_user', models.PositiveIntegerField()),
                ('users', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
            ],
        ),
    ]