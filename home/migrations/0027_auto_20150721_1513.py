# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_auto_20150721_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raidprogress',
            name='order',
            field=models.IntegerField(default=0, help_text='Order in which the raid was introduced to the game'),
            preserve_default=True,
        ),
    ]
