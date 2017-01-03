# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import annoying.fields
import pybb.util
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('size', models.IntegerField(verbose_name='Size')),
                ('file', models.FileField(verbose_name='File', upload_to=pybb.util.FilePathGenerator(to='pybb_upload\\attachments'))),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachments',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Name', max_length=80)),
                ('position', models.IntegerField(verbose_name='Position', default=0, blank=True)),
                ('hidden', models.BooleanField(verbose_name='Hidden', default=False, help_text='If checked, this category will be visible only for staff')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Name', max_length=80)),
                ('position', models.IntegerField(verbose_name='Position', default=0, blank=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('updated', models.DateTimeField(verbose_name='Updated', null=True, blank=True)),
                ('post_count', models.IntegerField(verbose_name='Post count', default=0, blank=True)),
                ('topic_count', models.IntegerField(verbose_name='Topic count', default=0, blank=True)),
                ('hidden', models.BooleanField(verbose_name='Hidden', default=False)),
                ('headline', models.TextField(verbose_name='Headline', null=True, blank=True)),
                ('category', models.ForeignKey(verbose_name='Category', to='pybb.Category', related_name='forums')),
                ('moderators', models.ManyToManyField(verbose_name='Moderators', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('parent', models.ForeignKey(verbose_name='Parent forum', null=True, to='pybb.Forum', blank=True, related_name='child_forums')),
            ],
            options={
                'verbose_name': 'Forum',
                'verbose_name_plural': 'Forums',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='ForumReadTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('time_stamp', models.DateTimeField(auto_now=True)),
                ('forum', models.ForeignKey(null=True, to='pybb.Forum', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Forum read tracker',
                'verbose_name_plural': 'Forum read trackers',
            },
        ),
        migrations.CreateModel(
            name='PollAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('text', models.CharField(verbose_name='Text', max_length=255)),
            ],
            options={
                'verbose_name': 'Poll answer',
                'verbose_name_plural': 'Polls answers',
            },
        ),
        migrations.CreateModel(
            name='PollAnswerUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('poll_answer', models.ForeignKey(verbose_name='Poll answer', to='pybb.PollAnswer', related_name='users')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL, related_name='poll_answers')),
            ],
            options={
                'verbose_name': 'Poll answer user',
                'verbose_name_plural': 'Polls answers users',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('body', models.TextField(verbose_name='Message')),
                ('body_html', models.TextField(verbose_name='HTML version')),
                ('body_text', models.TextField(verbose_name='Text version')),
                ('created', models.DateTimeField(verbose_name='Created', db_index=True, blank=True)),
                ('updated', models.DateTimeField(verbose_name='Updated', null=True, blank=True)),
                ('user_ip', models.IPAddressField(verbose_name='User IP', default='0.0.0.0', blank=True)),
                ('on_moderation', models.BooleanField(verbose_name='On moderation', default=False)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('signature', models.TextField(verbose_name='Signature', max_length=1024, blank=True)),
                ('signature_html', models.TextField(verbose_name='Signature HTML Version', max_length=1054, blank=True)),
                ('time_zone', models.FloatField(verbose_name='Time zone', default=4.0, choices=[(-9.0, '-11'), (-8.0, '-10'), (-7.0, '-09'), (-6.0, '-08'), (-5.0, '-07 PST'), (-4.0, '-06 MST'), (-3.0, '-05 CST'), (-2.0, '-04 EST'), (-1.0, '-03 AST'), (0.0, '-02 ADT'), (1.0, '-01'), (2.0, '+00'), (3.0, '01 GMT'), (4.0, '+02 CET'), (5.0, '+03'), (6.0, '+04'), (7.0, '+05'), (8.0, '+06'), (9.0, '+07'), (10.0, '+08'), (11.0, '+09'), (12.0, '+10'), (13.0, '+11'), (14.0, '+12'), (15.0, '+13'), (16.0, '+14'), (17.0, '+15')])),
                ('language', models.CharField(verbose_name='Language', max_length=10, default='en-us', choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-cn', 'Simplified Chinese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese'), ('zh-tw', 'Traditional Chinese')], blank=True)),
                ('show_signatures', models.BooleanField(verbose_name='Show signatures', default=True)),
                ('post_count', models.IntegerField(verbose_name='Post count', default=0, blank=True)),
                ('avatar', sorl.thumbnail.fields.ImageField(verbose_name='Avatar', null=True, upload_to=pybb.util.FilePathGenerator(to='pybb/avatar'), blank=True)),
                ('autosubscribe', models.BooleanField(verbose_name='Automatically subscribe', default=False, help_text='Automatically subscribe to topics that you answer')),
                ('user', annoying.fields.AutoOneToOneField(verbose_name='User', to=settings.AUTH_USER_MODEL, related_name='pybb_profile')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Subject', max_length=255)),
                ('created', models.DateTimeField(verbose_name='Created', null=True)),
                ('updated', models.DateTimeField(verbose_name='Updated', null=True)),
                ('views', models.IntegerField(verbose_name='Views count', default=0, blank=True)),
                ('sticky', models.BooleanField(verbose_name='Sticky', default=False)),
                ('closed', models.BooleanField(verbose_name='Closed', default=False)),
                ('post_count', models.IntegerField(verbose_name='Post count', default=0, blank=True)),
                ('on_moderation', models.BooleanField(verbose_name='On moderation', default=False)),
                ('poll_type', models.IntegerField(verbose_name='Poll type', default=0, choices=[(0, 'None'), (1, 'Single answer'), (2, 'Multiple answers')])),
                ('poll_question', models.TextField(verbose_name='Poll question', null=True, blank=True)),
                ('forum', models.ForeignKey(verbose_name='Forum', to='pybb.Forum', related_name='topics')),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='TopicReadTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('time_stamp', models.DateTimeField(auto_now=True)),
                ('topic', models.ForeignKey(null=True, to='pybb.Topic', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Topic read tracker',
                'verbose_name_plural': 'Topic read trackers',
            },
        ),
        migrations.AddField(
            model_name='topic',
            name='readed_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='readed_topics', through='pybb.TopicReadTracker'),
        ),
        migrations.AddField(
            model_name='topic',
            name='subscribers',
            field=models.ManyToManyField(verbose_name='Subscribers', related_name='subscriptions', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(verbose_name='Topic', to='pybb.Topic', related_name='posts'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL, related_name='posts'),
        ),
        migrations.AddField(
            model_name='pollanswer',
            name='topic',
            field=models.ForeignKey(verbose_name='Topic', to='pybb.Topic', related_name='poll_answers'),
        ),
        migrations.AddField(
            model_name='forum',
            name='readed_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='readed_forums', through='pybb.ForumReadTracker'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='post',
            field=models.ForeignKey(verbose_name='Post', to='pybb.Post', related_name='attachments'),
        ),
        migrations.AlterUniqueTogether(
            name='topicreadtracker',
            unique_together=set([('user', 'topic')]),
        ),
        migrations.AlterUniqueTogether(
            name='pollansweruser',
            unique_together=set([('poll_answer', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='forumreadtracker',
            unique_together=set([('user', 'forum')]),
        ),
    ]
