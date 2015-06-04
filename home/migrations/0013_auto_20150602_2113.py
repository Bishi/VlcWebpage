# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_member_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='thumbnail',
            field=models.CharField(blank=True, max_length=100),
            preserve_default=True,
        ),
    ]
