# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20150828_0328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='champion',
            name='post_fighter',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='post_mage',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='post_marksman',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='post_support',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='post_tank',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='pre_fighter',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='pre_mage',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='pre_marksman',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='pre_support',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='pre_tank',
        ),
        migrations.AddField(
            model_name='champion',
            name='post_roles',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='champion',
            name='pre_roles',
            field=models.TextField(default=b''),
        ),
    ]
