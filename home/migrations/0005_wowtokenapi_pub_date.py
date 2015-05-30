# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_wowtokenapi'),
    ]

    operations = [
        migrations.AddField(
            model_name='wowtokenapi',
            name='pub_date',
            field=models.DateTimeField(blank=True, verbose_name='date published', null=True),
            preserve_default=True,
        ),
    ]
