# Generated by Django 2.1.5 on 2019-01-30 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0006_auto_20190130_0801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newhero',
            name='user',
        ),
        migrations.RemoveField(
            model_name='newitem',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='agility',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='critic_chance',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='defense',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='dodge_chance',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='experience',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='health',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='intelligence',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='level',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='magic_attack',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='magic_resist',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='physical_attack',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='strength',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='vitality',
        ),
        migrations.RemoveField(
            model_name='item',
            name='agility',
        ),
        migrations.RemoveField(
            model_name='item',
            name='critic_chance',
        ),
        migrations.RemoveField(
            model_name='item',
            name='defense',
        ),
        migrations.RemoveField(
            model_name='item',
            name='dodge_chance',
        ),
        migrations.RemoveField(
            model_name='item',
            name='health',
        ),
        migrations.RemoveField(
            model_name='item',
            name='intelligence',
        ),
        migrations.RemoveField(
            model_name='item',
            name='magic_attack',
        ),
        migrations.RemoveField(
            model_name='item',
            name='magic_resist',
        ),
        migrations.RemoveField(
            model_name='item',
            name='physical_attack',
        ),
        migrations.RemoveField(
            model_name='item',
            name='strength',
        ),
        migrations.RemoveField(
            model_name='item',
            name='vitality',
        ),
        migrations.AddField(
            model_name='hero',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='herostatistic',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Hero'),
        ),
        migrations.AlterField(
            model_name='itemstatistic',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Item'),
        ),
        migrations.DeleteModel(
            name='NewHero',
        ),
        migrations.DeleteModel(
            name='NewItem',
        ),
    ]