from django.conf.urls import patterns, include, url
from django.contrib import admin
from home.views import home_redirect
from django.conf import settings
import VLCwebsite.views
import account.views

from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^$', 'home.views.index_view', name='home'),
    url(r'^articles/', include('home.urls', namespace="home")),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, },
        name="media"),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, },
        name="static"),

    # aliases to match original django-registration urls
    url(r"^account/", include("account.urls")),
    url(r"^accounts/signup/$", account.views.SignupView.as_view(), name="registration_register"),
    url(r"^accounts/login/$", account.views.LoginView.as_view(), name="auth_login"),
    url(r"^accounts/password/$", account.views.ChangePasswordView.as_view(), name="auth_password_change"),
    (r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^roster/$', 'home.views.roster', name='roster'),
    url(r'^chatarchive/$', 'home.views.chatterbox_archive', name='chatterbox_archive'),

    url(r'^captcha/', include('captcha.urls')),
    url(r'^apply/', 'home.views.application_info', name='apply'),
    url(r'^deletechat/(?P<chat_id>\d+)/$', 'home.views.delete_chatterbox', name='delete_chatterbox'),
    url(r'^deletecomment/(?P<comment_id>\d+)/$', 'home.views.delete_comment', name='delete_comment'),
)
