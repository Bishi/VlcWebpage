# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_wowtokenapi_pub_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=20)),
                ('spec', models.TextField(max_length=25)),
                ('rank', models.IntegerField()),
                ('player_class', models.TextField(max_length=15)),
                ('level', models.IntegerField()),
                ('timestamp', models.DateTimeField(verbose_name='timestamp')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
