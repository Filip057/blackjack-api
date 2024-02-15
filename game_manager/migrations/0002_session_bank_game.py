# Generated by Django 5.0.2 on 2024-02-13 12:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='bank',
            field=models.IntegerField(default=1000),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_over', models.BooleanField(default=False)),
                ('bet_placed', models.BooleanField(default=False)),
                ('bet', models.PositiveIntegerField(choices=[(10, '10'), (20, '25'), (50, '50'), (75, '75'), (100, '100')])),
                ('player_hand', models.JSONField()),
                ('dealer_hand', models.JSONField()),
                ('winner', models.CharField(default=None, max_length=50)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_manager.session')),
            ],
        ),
    ]