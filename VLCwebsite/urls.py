from django.conf.urls import patterns, include, url
from django.contrib import admin
from home.views import home_redirect
from django.conf import settings
import VLCwebsite.views
import account.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'VLCwebsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^$', home_redirect),
    url(r'^$', 'home.views.index_view',name='home'),
    url(r'^articles/', include('home.urls', namespace="home")),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),

    # aliases to match original django-registration urls
    url(r"^account/", include("account.urls")),
    url(r"^accounts/signup/$", account.views.SignupView.as_view(), name="registration_register"),
    url(r"^accounts/login/$", account.views.LoginView.as_view(), name="auth_login"),
    url(r"^accounts/password/$", account.views.ChangePasswordView.as_view(), name="auth_password_change"),
    (r'^forum/', include('pybb.urls', namespace='pybb')),

)
