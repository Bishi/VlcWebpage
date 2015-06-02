# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20150602_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='player_class_string',
            field=models.CharField(max_length=15, default='Unknown'),
            preserve_default=True,
        ),
    ]
