# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20150818_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='champion',
            name='bans',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='champion',
            name='picks',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='champion',
            name='wins',
            field=models.IntegerField(default=0),
        ),
    ]
