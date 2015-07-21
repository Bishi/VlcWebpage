# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_auto_20150721_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raidprogress',
            name='order',
            field=models.IntegerField(default=0, help_text='Chronological order of raid instances.'),
            preserve_default=True,
        ),
    ]
