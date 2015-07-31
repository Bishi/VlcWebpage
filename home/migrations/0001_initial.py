# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('body', models.TextField(max_length=1000)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Chatterbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=140)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Chatterbox',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClassName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name_text', models.CharField(max_length=20)),
                ('pic', models.FileField(upload_to='class_thumbnails/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClassRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_role_text', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('spec', models.CharField(max_length=40, null=True)),
                ('rank', models.IntegerField()),
                ('rank_string', models.CharField(default='Wrong Rank', max_length=20)),
                ('player_class', models.IntegerField()),
                ('player_class_string', models.CharField(default='Unknown', max_length=15)),
                ('level', models.IntegerField()),
                ('item_level', models.CharField(max_length=20, blank=True, null=True)),
                ('timestamp', models.DateTimeField(verbose_name='timestamp')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('thumbnail', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('body', models.TextField(max_length=9000, blank=True)),
                ('body_html', models.TextField(max_length=9000, blank=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('likes', models.IntegerField(default=0)),
                ('thumbnail', models.ImageField(validators=[home.models.NewsArticle.validate_image], upload_to=home.models.get_upload_file_name, blank=True, null=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RaidBoss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('defeated', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Raid bosses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RaidProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('difficulty', models.CharField(choices=[('Normal', 'Normal'), ('Heroic', 'Heroic'), ('Mythic', 'Mythic')], max_length=30)),
                ('tier', models.IntegerField(default=0)),
                ('bosses', models.IntegerField(default=0, null=True)),
                ('defeated_bosses', models.IntegerField(default=0, null=True)),
                ('order', models.IntegerField(help_text='Chronological order of raid instances.', default=0)),
                ('thumbnail', models.FileField(upload_to='raid_thumbnail/', null=True)),
            ],
            options={
                'verbose_name_plural': 'Raid progress',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RealmStatusAPI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('queue', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Realm status api',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recruit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_text', models.CharField(max_length=20)),
                ('thumbnail', models.FileField(upload_to='class_thumbnails/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recruitment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.ForeignKey(to='home.ClassName')),
                ('class_role', models.ForeignKey(to='home.ClassRole')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Spec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spec_name', models.CharField(max_length=20)),
                ('thumbnail', models.FileField(upload_to='class_thumbnails/class_icons/')),
                ('is_needed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WarcraftlogsAPI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True)),
                ('title', models.CharField(max_length=20)),
                ('owner', models.CharField(max_length=20)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('zone', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Warcraftlogs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WarcraftlogsURL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Warcraftlogs url',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WowTokenApi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(max_length=10, blank=True)),
                ('timestamp', models.CharField(max_length=30)),
                ('pub_date', models.DateTimeField(verbose_name='date published', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'WoW Token api',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='recruit',
            name='spec1',
            field=models.ForeignKey(related_name='spec1', to='home.Spec'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recruit',
            name='spec2',
            field=models.ForeignKey(related_name='spec2', to='home.Spec'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recruit',
            name='spec3',
            field=models.ForeignKey(related_name='spec3', to='home.Spec'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='raidboss',
            name='raid_instance',
            field=models.ForeignKey(to='home.RaidProgress'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articlecomment',
            name='origin',
            field=models.ForeignKey(to='home.NewsArticle'),
            preserve_default=True,
        ),
    ]
