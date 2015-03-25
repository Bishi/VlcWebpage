# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pybb', '0004_auto_20150308_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='autosubscribe',
            field=models.BooleanField(help_text='Automatically subscribe to topics that you answer', default=False, verbose_name='Automatically subscribe'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='time_zone',
            field=models.FloatField(choices=[(-12.0, '-12'), (-11.0, '-11'), (-10.0, '-10'), (-9.5, '-09.5'), (-9.0, '-09'), (-8.5, '-08.5'), (-8.0, '-08 PST'), (-7.0, '-07 MST'), (-6.0, '-06 CST'), (-5.0, '-05 EST'), (-4.0, '-04 AST'), (-3.5, '-03.5'), (-3.0, '-03 ADT'), (-2.0, '-02'), (-1.0, '-01'), (0.0, '00 GMT'), (1.0, '+01 CET'), (2.0, '+02'), (3.0, '+03'), (3.5, '+03.5'), (4.0, '+04'), (4.5, '+04.5'), (5.0, '+05'), (5.5, '+05.5'), (6.0, '+06'), (6.5, '+06.5'), (7.0, '+07'), (8.0, '+08'), (9.0, '+09'), (9.5, '+09.5'), (10.0, '+10'), (10.5, '+10.5'), (11.0, '+11'), (11.5, '+11.5'), (12.0, '+12'), (13.0, '+13'), (14.0, '+14')], default=1.0, verbose_name='Time zone'),
            preserve_default=True,
        ),
    ]
