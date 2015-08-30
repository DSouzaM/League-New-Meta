# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20150828_0414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='champion',
            name='roles',
            field=models.TextField(default=b'{}'),
        ),
    ]
