# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20150602_2113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recruit',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name_text', models.CharField(max_length=20)),
                ('thumbnail', models.FileField(upload_to='class_thumbnails/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpecName',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('spec_name', models.CharField(max_length=20)),
                ('thumbnail', models.FileField(upload_to='class_thumbnails/class_icons/')),
                ('is_needed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='recruit',
            name='spec1',
            field=models.ForeignKey(to='home.SpecName', related_name='spec1'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recruit',
            name='spec2',
            field=models.ForeignKey(to='home.SpecName', related_name='spec2'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recruit',
            name='spec3',
            field=models.ForeignKey(to='home.SpecName', related_name='spec3'),
            preserve_default=True,
        ),
    ]
