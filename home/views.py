from django.utils import timezone
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from home.forms import NewsArticleForm
from home.models import NewsArticle, Recruitment, WarcraftlogsAPI, RealmStatusAPI
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from pybb.permissions import perms
from django.shortcuts import get_object_or_404
from pybb.models import Topic


#class IndexView(generic.TemplateView):
#    template_name = 'home/index.html'


#homepage
def index_view(request):
    #home
    if request.user:
        user = request.user
    else:
        user = None

    #group
    group_name = 'not_officer'
    if request.user.groups.filter(name='Officer'):
        group_name = 'Officer'

    #article_list
    article_list = NewsArticle.objects.all().order_by('-pub_date')

    #article pagination
    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    #recruitment ordering alphabetical
    recruitment_list = Recruitment.objects.all().order_by('class_name__class_name_text', 'class_role')

    #latest forum posts
    qs = Topic.objects.all().select_related().order_by('-updated', '-id')
    qs = perms.filter_topics(request.user, qs)
    qs = qs[:5]

    #warcraftlogs
    logs_list = WarcraftlogsAPI.objects.all().order_by('-end');
    logs_list = logs_list[:5]

    #realm status
    realm_status = RealmStatusAPI.objects.all()

    return render_to_response('home/index.html',
                             {'user': user,
                              'newsArticles': articles,
                              'recruitment': recruitment_list,
                              'group': group_name,
                              'topic_list': qs,
                              'logs_list': logs_list,
                              'realm_status': realm_status},)


def home_redirect(response):
    return HttpResponseRedirect('/')


#/home/all
def news_articles(request):
    #user
    if request.user:
        user = request.user
    else:
        user = None

    #group
    group_name = 'not_officer'
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
                              'user': user,
                              'group': group_name},)


def news_article(request, article_id=1):
    #user
    if request.user:
        user = request.user
    else:
        user = None

    #group
    group_name = 'not_officer'
    if request.user.groups.filter(name='Officer'):
        group_name = 'Officer'

    try:
        article = NewsArticle.objects.get(id=article_id)
    except:
        raise Http404("Article does not exist")


    instance = get_object_or_404(NewsArticle, id=article_id)
    form = NewsArticleForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/articles/all')

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['user'] = user
    args['group'] = group_name
    args['newsArticle'] = article

    #return render_to_response('home/news_article.html',
    #                         {'newsArticle': article,
    #                          'user': user,
    #                          'group': group_name,
    #                          'form': form})
    return render_to_response('home/news_article.html', args)



def create(request):
    #if user is not logged in, forbidden
    user = None
    if request.user:
        user = request.user
    if user is None:
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
    args['user'] = user

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
    #recruitment_list = Recruitment.objects.all()
    if request.user:
        user = request.user
    else:
        user = None

    logs_list = WarcraftlogsAPI.objects.all().order_by('-end');
    logs_list = logs_list[:5]

    return render_to_response('home/test_page.html',
                             {'user': user,
                              'logs_list': logs_list})


def application_info(request):
    #user
    if request.user:
        user = request.user
    else:
        user = None

    #group
    group_name = 'not_officer'
    if request.user.groups.filter(name='Officer'):
        group_name = 'Officer'


    return render_to_response('home/application_info.html',
                             {'user': user,
                              'group': group_name})