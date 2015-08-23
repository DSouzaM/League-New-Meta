# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_champion_role'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='champion',
            unique_together=set([('region', 'version', 'gamemode', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('region', 'version', 'gamemode', 'key')]),
        ),
    ]
