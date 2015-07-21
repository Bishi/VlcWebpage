# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_raidprogress_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='raidprogress',
            options={'verbose_name_plural': 'Raid progress'},
        ),
    ]
