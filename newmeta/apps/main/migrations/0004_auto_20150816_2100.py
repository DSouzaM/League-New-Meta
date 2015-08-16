# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_match_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='gamemode',
            field=models.CharField(default='NORMAL_5X5', max_length=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='patch',
            field=models.CharField(default='5.11', max_length=4),
            preserve_default=False,
        ),
    ]
