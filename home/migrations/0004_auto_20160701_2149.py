# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20160701_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruit',
            name='spec3',
            field=models.ForeignKey(null=True, blank=True, to='home.Spec', related_name='spec3'),
            preserve_default=True,
        ),
    ]
