# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20150601_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='spec',
            field=models.CharField(null=True, max_length=25),
            preserve_default=True,
        ),
    ]
