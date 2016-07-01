# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pybb', '0007_auto_20150404_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='time_zone',
            field=models.FloatField(choices=[(-9.0, '-12'), (-8.0, '-11'), (-7.0, '-10'), (-6.0, '-09'), (-5.0, '-08 PST'), (-4.0, '-07 MST'), (-3.0, '-06 CST'), (-2.0, '-05 EST'), (-1.0, '-04 AST'), (0.0, '-03 ADT'), (1.0, '-02'), (2.0, '-01'), (3.0, '00 GMT'), (4.0, '+01 CEST'), (5.0, '+02'), (6.0, '+03'), (7.0, '+04'), (8.0, '+05'), (9.0, '+06'), (10.0, '+07'), (11.0, '+08'), (12.0, '+09'), (13.0, '+10'), (14.0, '+11'), (15.0, '+12'), (16.0, '+13'), (17.0, '+14')], default=4.0, verbose_name='Time zone'),
            preserve_default=True,
        ),
    ]
