# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_auto_20150721_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='raidprogress',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
