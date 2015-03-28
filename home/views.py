from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import context
from home.forms import NewsArticleForm
from home.models import NewsArticle, Recruitment
from django.core.context_processors import csrf
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
import datetime
import account.views
import home.forms

#class IndexView(generic.TemplateView):
#    template_name = 'home/index.html'


#homepage
def index_view(request):
    #index
    user = None
    if request.user.username:
        user = request.user.username
    else:
        user = None

    #group
    group_name = 'not_officer';
    if request.user.groups.filter(name='Officer'):
        group_name = 'Officer'

    #article pagination
    article_list = NewsArticle.objects.all().order_by('-pub_date')
    #article_list.
    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    #recruitment ordering alphabetical
    recruitment_list = Recruitment.objects.all().order_by('class_name__class_name_text','class_role')

    return render_to_response('home/index.html',
                             {'username': user,
                              'newsArticles': articles,
                              'recruitment': recruitment_list,
                              'group':group_name},)


def home_redirect(response):
    return HttpResponseRedirect('/')


#/home/all
def news_articles(request):
    #user
    if request.user.username:
        user = request.user.username
    else:
        user = None

    #group
    group_name = 'not_officer';
    if request.user.groups.filter(name='Officer'):
        group_name = 'Officer'

    #list of articles
    article_list = NewsArticle.objects.all().order_by('-pub_date')
    paginator = Paginator(article_list, 5)

    page = request.GET.get('page')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render_to_response('home/news_articles.html',
                             {'newsArticles': articles,
                              'username': user,
                              'group': group_name},)


def news_article(request, article_id=1):
    #user
    user = None
    if request.user.username:
        user = request.user.username
    else:
        user = None

    #group
    group_name = 'not_officer';
    if request.user.groups.filter(name='Officer'):
        group_name = 'Officer'


    return render_to_response('home/news_article.html',
                             {'newsArticle': NewsArticle.objects.get(id=article_id),
                              'username': user,
                              'group': group_name})


def create(request):
    #if user is not logged in, forbidden
    user = None
    if request.user.username:
        user = request.user.username
    if user is None:
        #return HttpResponseForbidden()
        raise PermissionDenied()

    #if the user is not an officer, forbidden
    if not request.user.groups.filter(name='Officer'):
        raise PermissionDenied()

    if request.POST:
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            #form.save()
            instance = form.save(commit=False)
            instance.author = request.user
            instance.pub_date = timezone.now()
            instance.save()

            return HttpResponseRedirect('/articles/all')
    else:
        form = NewsArticleForm()
    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['username'] = user

    return render_to_response('home/create_news_article.html', args,)


def like_article(request, article_id):
    if article_id:
        a = NewsArticle.objects.get(id=article_id)
        count = a.likes
        count += 1
        a.likes = count
        a.save()
    return HttpResponseRedirect('/articles/get/%s' % article_id)


def test_page(request):
    recruitment_list = Recruitment.objects.all()

    return render_to_response('home/test_page.html',
                             {'recruitment': recruitment_list})

