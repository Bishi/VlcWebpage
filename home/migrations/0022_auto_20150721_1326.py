# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20150721_1324'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatterbox',
            options={'verbose_name_plural': 'Chatterbox'},
        ),
        migrations.AlterModelOptions(
            name='raidboss',
            options={'verbose_name_plural': 'Raid bosses'},
        ),
        migrations.AlterModelOptions(
            name='realmstatusapi',
            options={'verbose_name_plural': 'Realm Status Api'},
        ),
        migrations.AlterModelOptions(
            name='warcraftlogsurl',
            options={'verbose_name_plural': 'Warcraftlogs url'},
        ),
        migrations.AlterModelOptions(
            name='wowtokenapi',
            options={'verbose_name_plural': 'WoW Token api'},
        ),
    ]
