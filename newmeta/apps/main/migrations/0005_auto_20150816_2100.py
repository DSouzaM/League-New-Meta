# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150816_2100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='patch',
            new_name='version',
        ),
    ]
