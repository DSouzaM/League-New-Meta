# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20150821_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='champion',
            name='role',
            field=models.CharField(default=b'', max_length=8),
        ),
    ]
