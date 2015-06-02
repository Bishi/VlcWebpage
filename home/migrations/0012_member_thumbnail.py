# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20150602_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='thumbnail',
            field=models.CharField(blank=True, max_length=40),
            preserve_default=True,
        ),
    ]
