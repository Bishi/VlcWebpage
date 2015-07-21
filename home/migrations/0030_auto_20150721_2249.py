# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_auto_20150721_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='raidprogress',
            name='thumbnail',
            field=models.FileField(upload_to='raid_thumbnail/', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='raidprogress',
            name='bosses',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='raidprogress',
            name='defeated_bosses',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
    ]
