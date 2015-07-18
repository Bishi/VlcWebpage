# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20150607_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='item_level',
            field=models.CharField(null=True, max_length=20, blank=True),
            preserve_default=True,
        ),
    ]
