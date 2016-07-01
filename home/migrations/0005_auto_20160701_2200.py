# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20160701_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruit',
            name='spec3',
            field=models.ForeignKey(to='home.Spec', related_name='spec3'),
            preserve_default=True,
        ),
    ]
