# Generated by Django 5.0.1 on 2024-01-22 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0008_remove_listing_band_delete_band_delete_listing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PointP1', models.DecimalField(decimal_places=0, max_digits=10)),
                ('PointP2', models.DecimalField(decimal_places=0, max_digits=10)),
            ],
        ),
    ]