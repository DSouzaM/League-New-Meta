# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20150823_1655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='champion',
            name='bans',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='role',
        ),
        migrations.AddField(
            model_name='champion',
            name='post_fighter',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='champion',
            name='post_mage',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='champion',
            name='post_marksman',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='champion',
            name='post_support',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='champion',
            name='post_tank',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='champion',
            name='pre_fighter',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='champion',
            name='pre_mage',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='champion',
            name='pre_marksman',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='champion',
            name='pre_support',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='champion',
            name='pre_tank',
            field=models.FloatField(default=0.0),
        ),
    ]
