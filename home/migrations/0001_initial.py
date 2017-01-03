# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import home.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('body', models.TextField(max_length=1000)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chatterbox',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(max_length=140)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Chatterbox',
            },
        ),
        migrations.CreateModel(
            name='EndpointUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Endpoint Urls',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('spec', models.CharField(null=True, max_length=40)),
                ('rank', models.IntegerField()),
                ('rank_string', models.CharField(default='Wrong Rank', max_length=20)),
                ('player_class', models.IntegerField()),
                ('player_class_string', models.CharField(default='Unknown', max_length=15)),
                ('level', models.IntegerField()),
                ('item_level', models.CharField(null=True, blank=True, max_length=20)),
                ('timestamp', models.DateTimeField(verbose_name='timestamp')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('thumbnail', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('body', models.TextField(blank=True, max_length=9000)),
                ('body_html', models.TextField(blank=True, max_length=9000)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('likes', models.IntegerField(default=0)),
                ('thumbnail', models.ImageField(null=True, blank=True, validators=[home.models.NewsArticle.validate_image], upload_to=home.models.get_upload_file_name)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RaidBoss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('defeated', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Raid bosses',
            },
        ),
        migrations.CreateModel(
            name='RaidProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('difficulty', models.CharField(choices=[('Normal', 'Normal'), ('Heroic', 'Heroic'), ('Mythic', 'Mythic')], max_length=30)),
                ('tier', models.IntegerField(default=0)),
                ('bosses', models.IntegerField(default=0, null=True)),
                ('defeated_bosses', models.IntegerField(default=0, null=True)),
                ('order', models.IntegerField(help_text='Chronological order of raid instances.', default=0)),
                ('thumbnail', models.FileField(null=True, upload_to='raid_thumbnail/')),
            ],
            options={
                'verbose_name_plural': 'Raid progress',
            },
        ),
        migrations.CreateModel(
            name='RealmStatusAPI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(null=True, max_length=200)),
                ('queue', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Realm status api',
            },
        ),
        migrations.CreateModel(
            name='Recruit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_text', models.CharField(max_length=20)),
                ('thumbnail', models.FileField(upload_to='class_thumbnails/')),
            ],
        ),
        migrations.CreateModel(
            name='Spec',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('spec_name', models.CharField(max_length=25)),
                ('thumbnail', models.FileField(upload_to='class_thumbnails/class_icons/')),
                ('is_needed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WarcraftlogsAPI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(null=True, max_length=20)),
                ('title', models.CharField(max_length=20)),
                ('owner', models.CharField(max_length=20)),
                ('start', models.BigIntegerField()),
                ('end', models.BigIntegerField()),
                ('zone', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Warcraftlogs',
            },
        ),
        migrations.CreateModel(
            name='WarcraftlogsURL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Warcraftlogs url',
            },
        ),
        migrations.CreateModel(
            name='WowTokenApi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.CharField(blank=True, max_length=10)),
                ('timestamp', models.CharField(max_length=30)),
                ('pub_date', models.DateTimeField(verbose_name='date published', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'WoW Token api',
            },
        ),
        migrations.AddField(
            model_name='recruit',
            name='spec1',
            field=models.ForeignKey(related_name='spec1', to='home.Spec'),
        ),
        migrations.AddField(
            model_name='recruit',
            name='spec2',
            field=models.ForeignKey(related_name='spec2', to='home.Spec'),
        ),
        migrations.AddField(
            model_name='recruit',
            name='spec3',
            field=models.ForeignKey(related_name='spec3', to='home.Spec'),
        ),
        migrations.AddField(
            model_name='raidboss',
            name='raid_instance',
            field=models.ForeignKey(to='home.RaidProgress'),
        ),
        migrations.AddField(
            model_name='articlecomment',
            name='origin',
            field=models.ForeignKey(to='home.NewsArticle'),
        ),
    ]
