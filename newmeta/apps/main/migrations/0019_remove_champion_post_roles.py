# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20150828_0335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='champion',
            name='post_roles',
        ),
    ]
