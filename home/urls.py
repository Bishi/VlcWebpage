from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'home.views.home_redirect'),
    url(r'^all/$', 'home.views.news_articles', name='articles'),
    url(r'^get/(?P<article_id>\d+)/$', 'home.views.news_article', name='article'),
    url(r'^delete/(?P<article_id>\d+)/$', 'home.views.delete_article', name='delete_article'),
    url(r'^create/$', 'home.views.create', name='create_article'),
    # url(r'^test/$', 'home.views.test_page', name='test_page'),
)