# Generated by Django 2.1.3 on 2019-01-18 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20190117_2338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='minimal_level',
        ),
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='game.Hero'),
            preserve_default=False,
        ),
    ]