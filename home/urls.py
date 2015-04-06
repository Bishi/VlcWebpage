from django.conf.urls import patterns, url

urlpatterns = patterns('',
    #url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^$', 'home.views.index_view'),
    url(r'^$', 'home.views.home_redirect'),
    url(r'^all/$', 'home.views.news_articles'),
    url(r'^get/(?P<article_id>\d+)/$', 'home.views.news_article'),
    url(r'^delete/(?P<article_id>\d+)/$', 'home.views.delete_article'),
    url(r'^create/$', 'home.views.create'),
    #url(r'^like/(?P<article_id>\d+)/$', 'home.views.like_article'),
    url(r'^test/$', 'home.views.test_page', name='topic_latest'),
    #url('^test/$', home.views.LatestTopicsView.as_view(), name='topic_latest'),
)