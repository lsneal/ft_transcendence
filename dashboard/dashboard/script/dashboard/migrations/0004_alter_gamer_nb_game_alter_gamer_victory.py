
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_gamer_nb_game_alter_gamer_victory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamer',
            name='nb_game',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gamer',
            name='victory',
            field=models.IntegerField(default=0),
        ),
    ]
