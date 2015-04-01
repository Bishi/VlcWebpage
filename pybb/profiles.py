# coding=utf-8
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import ugettext_lazy as _
from pybb import defaults, util
from pybb.compat import get_image_field_class, get_username_field


TZ_CHOICES = [(float(x[0]), x[1]) for x in (
    (-10, '-12'), (-9, '-11'), (-8, '-10'), (-7, '-09'),
    (-6, '-08 PST'), (-5, '-07 MST'), (-4, '-06 CST'),
    (-3, '-05 EST'), (-2, '-04 AST'), (-1, '-03 ADT'),
    (0, '-02'), (1, '-01'), (2, '00 GMT'), (3, '+01 CET'), (4, '+02'),
    (5, '+03'), (6, '+04'), (7, '+05'),
    (8, '+06'), (9, '+07'), (10, '+08'),
    (11, '+09'), (12, '+10'), (13, '+11'),
    (14, '+12'), (15, '+13'), (16, '+14'),
)]

TZ_CHOICES2 = [(float(x[0]), x[1]) for x in (
    (-9, '-12'), (-8, '-11'), (-7, '-10'), (-6, '-09'),
    (-5, '-08 PST'), (-4, '-07 MST'), (-3, '-06 CST'),
    (-2, '-05 EST'), (-1, '-04 AST'), (0, '-03 ADT'),
    (1, '-02'), (2, '-01'), (3, '00 GMT'), (4, '+01 CET'), (5, '+02'),
    (6, '+03'), (7, '+04'), (8, '+05'),
    (9, '+06'), (10, '+07'), (11, '+08'),
    (12, '+09'), (13, '+10'), (14, '+11'),
    (15, '+12'), (16, '+13'), (17, '+14'),
)]


class PybbProfile(models.Model):
    """
    Abstract class for user profile, site profile should be inherted from this class
    """

    class Meta(object):
        abstract = True
        permissions = (
            ("block_users", "Can block any user"),
        )

    signature = models.TextField(_('Signature'), blank=True, max_length=defaults.PYBB_SIGNATURE_MAX_LENGTH)
    signature_html = models.TextField(_('Signature HTML Version'), blank=True,
                                      max_length=defaults.PYBB_SIGNATURE_MAX_LENGTH + 30)
    time_zone = models.FloatField(_('Time zone'), choices=TZ_CHOICES2, default=float(defaults.PYBB_DEFAULT_TIME_ZONE))
    language = models.CharField(_('Language'), max_length=10, blank=True, choices=settings.LANGUAGES,
                                default=settings.LANGUAGE_CODE)
    show_signatures = models.BooleanField(_('Show signatures'), blank=True, default=True)
    post_count = models.IntegerField(_('Post count'), blank=True, default=0)
    avatar = get_image_field_class()(_('Avatar'), blank=True, null=True,
                                     upload_to=util.FilePathGenerator(to='pybb/avatar'))
    autosubscribe = models.BooleanField(_('Automatically subscribe'),
                                        help_text=_('Automatically subscribe to topics that you answer'),
                                        default=defaults.PYBB_DEFAULT_AUTOSUBSCRIBE)

    def save(self, *args, **kwargs):
        self.signature_html = util._get_markup_formatter()(self.signature)
        super(PybbProfile, self).save(*args, **kwargs)

    @property
    def avatar_url(self):
        try:
            return self.avatar.url
        except:
            return defaults.PYBB_DEFAULT_AVATAR_URL

    def get_display_name(self):
        try:
            if hasattr(self, 'user'):  # we have OneToOne foreign key to user model
                return self.user.get_username()
            if not defaults.PYBB_PROFILE_RELATED_NAME:  # we now in user custom model itself
                return self.get_username()
        except Exception:
            return unicode(self)
