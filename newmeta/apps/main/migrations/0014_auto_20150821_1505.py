# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_item'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='champion',
            unique_together=set([('region', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('region', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='match',
            unique_together=set([('region', 'match_id')]),
        ),
    ]
