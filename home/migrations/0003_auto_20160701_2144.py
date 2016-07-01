# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20150731_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruitment',
            name='class_name',
        ),
        migrations.DeleteModel(
            name='ClassName',
        ),
        migrations.RemoveField(
            model_name='recruitment',
            name='class_role',
        ),
        migrations.DeleteModel(
            name='ClassRole',
        ),
        migrations.DeleteModel(
            name='Recruitment',
        ),
        migrations.AlterField(
            model_name='recruit',
            name='spec3',
            field=models.ForeignKey(to='home.Spec', related_name='spec3', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spec',
            name='spec_name',
            field=models.CharField(max_length=25),
            preserve_default=True,
        ),
    ]
