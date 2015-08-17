# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_gamemode_region_version'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='gamemode',
            new_name='gamemode2',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='region',
            new_name='region2',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='version',
            new_name='version2',
        ),
    ]
