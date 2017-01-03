from django.conf.urls import url
from home import views

urlpatterns  = [
    url(r'^$', views.home_redirect),
    url(r'^all/$', views.news_articles, name='articles'),
    url(r'^get/(?P<article_id>\d+)/$', views.news_article, name='article'),
    url(r'^delete/(?P<article_id>\d+)/$', views.delete_article, name='delete_article'),
    url(r'^create/$', views.create, name='create_article'),
    # url(r'^test/$', 'home.views.test_page', name='test_page'),
]