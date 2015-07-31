# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warcraftlogsapi',
            name='end',
            field=models.BigIntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='warcraftlogsapi',
            name='start',
            field=models.BigIntegerField(),
            preserve_default=True,
        ),
    ]
