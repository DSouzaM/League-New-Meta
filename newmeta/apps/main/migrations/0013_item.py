# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20150818_0249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.IntegerField()),
                ('name', models.CharField(max_length=16)),
                ('wins', models.IntegerField(default=0)),
                ('picks', models.IntegerField(default=0)),
                ('gamemode', models.ForeignKey(default=1, to='main.Gamemode')),
                ('region', models.ForeignKey(default=1, to='main.Region')),
                ('version', models.ForeignKey(default=1, to='main.Version')),
            ],
        ),
    ]
