# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_auto_20150721_1326'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='raidboss',
            options={'verbose_name_plural': 'Raid Bosses'},
        ),
        migrations.AlterModelOptions(
            name='raidprogress',
            options={'verbose_name_plural': 'Raid Progress'},
        ),
    ]
