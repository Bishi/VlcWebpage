# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_auto_20150721_1326'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='realmstatusapi',
            options={'verbose_name_plural': 'Realm Status api'},
        ),
        migrations.AlterModelOptions(
            name='warcraftlogsapi',
            options={'verbose_name_plural': 'Warcraftlogs'},
        ),
    ]
