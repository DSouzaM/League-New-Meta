# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_remove_champion_post_roles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='champion',
            old_name='pre_roles',
            new_name='roles',
        ),
    ]
