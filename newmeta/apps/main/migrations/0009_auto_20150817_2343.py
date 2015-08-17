# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20150817_2301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='gamemode2',
        ),
        migrations.RemoveField(
            model_name='match',
            name='region2',
        ),
        migrations.RemoveField(
            model_name='match',
            name='version2',
        ),
    ]
