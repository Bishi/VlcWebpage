# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20150721_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='raidprogress',
            name='bosses',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='raidprogress',
            name='defeated_bosses',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='raidprogress',
            name='tier',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
