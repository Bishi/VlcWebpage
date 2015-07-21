# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_auto_20150721_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raidprogress',
            name='difficulty',
            field=models.CharField(max_length=30, choices=[('Normal', 'Normal'), ('Heroic', 'Heroic'), ('Mythic', 'Mythic')]),
            preserve_default=True,
        ),
    ]
