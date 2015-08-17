# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20150817_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='gamemode',
            field=models.ForeignKey(default=1, to='main.Gamemode'),
        ),
        migrations.AddField(
            model_name='match',
            name='region',
            field=models.ForeignKey(default=1, to='main.Region'),
        ),
        migrations.AddField(
            model_name='match',
            name='version',
            field=models.ForeignKey(default=1, to='main.Version'),
        ),
    ]
