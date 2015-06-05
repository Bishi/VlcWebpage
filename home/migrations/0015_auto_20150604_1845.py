# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20150604_1115'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SpecName',
            new_name='Spec',
        ),
    ]
