# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20150601_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='player_class_string',
            field=models.CharField(default='None', max_length=15),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='rank_string',
            field=models.CharField(default='Wrong Rank', max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='player_class',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
