# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_newsarticle_body_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='body_html',
            field=models.TextField(blank=True, max_length=9000),
            preserve_default=True,
        ),
    ]
