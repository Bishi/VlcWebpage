from django.db import models
from time import time
import time
from django.core.exceptions import ValidationError
from pybb.util import _get_markup_formatter


def get_upload_file_name(instance, filename):
    return "uploaded_files/%s_%s" % (str(time.time()).replace('.', '_'), filename)


class NewsArticle(models.Model):
    #image size limit
    def validate_image(self):
        file_size = self.file.size
        megabyte_limit = 5.0
        if file_size > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    title = models.CharField(max_length=30)
    body = models.TextField(max_length=9000, blank=True)
    body_html = models.TextField(max_length=9000, blank=True)
    pub_date = models.DateTimeField('date published')
    likes = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to=get_upload_file_name, null=True, blank=True, validators=[validate_image])
    author = models.ForeignKey('auth.User')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        #self.body_html = BaseParser().format(self.body)
        self.body_html = _get_markup_formatter()(self.body)
        super(NewsArticle, self).save(*args, **kwargs)


class ArticleComment(models.Model):
    author = models.ForeignKey('auth.User')
    pub_date = models.DateTimeField('date published')
    body = models.TextField(max_length=1000)
    origin = models.ForeignKey(NewsArticle)

    def __str__(self):
        return self.body


class Spec(models.Model):
    spec_name = models.CharField(max_length=20)
    thumbnail = models.FileField(upload_to="class_thumbnails/class_icons/")
    is_needed = models.BooleanField(default=False)

    def __str__(self):
        return self.spec_name


class Recruit(models.Model):
    name_text = models.CharField(max_length=20)
    thumbnail = models.FileField(upload_to="class_thumbnails/")
    spec1 = models.ForeignKey(Spec, related_name="spec1")
    spec2 = models.ForeignKey(Spec, related_name="spec2")
    spec3 = models.ForeignKey(Spec, related_name="spec3")

    def __str__(self):
        return self.name_text


class WarcraftlogsAPI(models.Model):
    name = models.CharField(max_length=20, null=True)
    title = models.CharField(max_length=20)
    owner = models.CharField(max_length=20)
    start = models.BigIntegerField()
    end = models.BigIntegerField()
    zone = models.IntegerField()

    def __str__(self):
        #return self.title
        return '%s %s' % (self.name, self.title)

    class Meta:
        verbose_name_plural = "Warcraftlogs"


class WarcraftlogsURL(models.Model):
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name_plural = "Warcraftlogs url"


class RealmStatusAPI(models.Model):
    name = models.CharField(max_length=200, null=True)
    queue = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Realm status api"


class WowTokenApi(models.Model):
    price = models.CharField(max_length=10, blank=True)
    timestamp = models.CharField(max_length=30)
    pub_date = models.DateTimeField('date published', blank=True, null=True)

    def __str__(self):
        return self.timestamp

    class Meta:
        verbose_name_plural = "WoW Token api"


class Chatterbox(models.Model):
    author = models.ForeignKey('auth.User')
    body = models.TextField(max_length=140)
    pub_date = models.DateTimeField('date published')

    class Meta:
        verbose_name_plural = "Chatterbox"


def get_rank(rank):
    # current_ranks = ['Guild Master', 'Officer', 'Officer Alt',
    #                  'Member', 'Trial', 'Alt', 'Slacker', 'STFU', 'Wrong Rank']
    current_ranks = ['Guild Master', 'Officer', 'Officer Alt',
                     'Raider', 'Member', 'Backup/AFK', 'Trial', 'Alt', 'Social', 'Wrong Rank']
    try:
        c_string = current_ranks[rank]
    except:
        c_string = 'Unknown'

    return c_string


def get_class(player_class):
    classes = ['Unknown', 'Warrior', 'Paladin', 'Hunter', 'Rogue',
               'Priest', 'Death Knight', 'Shaman', 'Mage', 'Warlock', 'Monk', 'Druid']
    try:
        c_string = classes[player_class]
    except:
        c_string = 'Unknown'

    return c_string


class Member(models.Model):
    name = models.CharField(max_length=20)
    spec = models.CharField(max_length=40, null=True)
    rank = models.IntegerField()
    rank_string = models.CharField(max_length=20, default="Wrong Rank")
    player_class = models.IntegerField()
    player_class_string = models.CharField(max_length=15, default="Unknown")
    level = models.IntegerField()
    item_level = models.CharField(max_length=20, null=True, blank=True)
    timestamp = models.DateTimeField('timestamp')
    pub_date = models.DateTimeField('date published')
    thumbnail = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.player_class_string = get_class(self.player_class)
        self.rank_string = get_rank(self.rank)
        super(Member, self).save(*args, **kwargs)


class RaidProgress(models.Model):
    name = models.CharField(max_length=30)
    difficulty = models.CharField(max_length=30, choices=[('Normal', 'Normal'), ('Heroic', 'Heroic'),
                                                          ('Mythic', 'Mythic')])
    tier = models.IntegerField(default=0)
    bosses = models.IntegerField(default=0, null=True)
    defeated_bosses = models.IntegerField(default=0, null=True)
    order = models.IntegerField(default=0, help_text='Chronological order of raid instances.')
    thumbnail = models.FileField(upload_to="raid_thumbnail/", null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        raid_bosses = RaidBoss.objects.all()
        boss_count = 0
        defeated_count = 0
        for boss in raid_bosses:
            if boss.raid_instance.name == self.name and boss.raid_instance.difficulty == self.difficulty:
                boss_count += 1
        for boss in raid_bosses:
            if boss.raid_instance.name == self.name and boss.raid_instance.difficulty == self.difficulty\
                    and boss.defeated:
                defeated_count += 1
        self.bosses = boss_count
        self.defeated_bosses = defeated_count
        super(RaidProgress, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Raid progress"


class RaidBoss(models.Model):
    raid_instance = models.ForeignKey(RaidProgress)
    name = models.CharField(max_length=30)
    defeated = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Raid bosses"
