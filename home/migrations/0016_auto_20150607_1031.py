# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20150604_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='spec',
            field=models.CharField(max_length=40, null=True),
            preserve_default=True,
        ),
    ]
