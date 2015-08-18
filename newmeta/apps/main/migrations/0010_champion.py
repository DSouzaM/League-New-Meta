# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20150817_2343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('key', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=16)),
                ('wins', models.IntegerField()),
                ('picks', models.IntegerField()),
                ('bans', models.IntegerField()),
                ('gamemode', models.ForeignKey(default=1, to='main.Gamemode')),
                ('region', models.ForeignKey(default=1, to='main.Region')),
                ('version', models.ForeignKey(default=1, to='main.Version')),
            ],
        ),
    ]
