# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_auto_20150721_1327'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='raidboss',
            options={'verbose_name_plural': 'Raid bosses'},
        ),
        migrations.AlterModelOptions(
            name='raidprogress',
            options={'verbose_name_plural': 'Raid progress'},
        ),
        migrations.AlterModelOptions(
            name='realmstatusapi',
            options={'verbose_name_plural': 'Realm status api'},
        ),
    ]
