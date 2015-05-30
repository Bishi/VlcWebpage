# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_newsarticle_body_html'),
    ]

    operations = [
        migrations.CreateModel(
            name='WoWTokenApi',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(blank=True, max_length=10)),
                ('timestamp', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
