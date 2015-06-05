from django.utils import timezone
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from home.forms import NewsArticleForm, DeleteNewsArticleForm, ChatterboxForm, ChatterboxDeleteForm, DeleteCommentForm, CommentForm
from home.models import NewsArticle, Recruitment, WarcraftlogsAPI, WowTokenApi, Chatterbox, ArticleComment, Member, Recruit
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from pybb.permissions import perms
from django.shortcuts import get_object_or_404
from pybb.models import Topic
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
import bbcode
from django.utils.safestring import mark_safe


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

    #recruit
    recruits = Recruit.objects.all().order_by('name_text')

    #latest forum posts
    qs = Topic.objects.all().select_related().order_by('-updated', '-id')
    qs = perms.filter_topics(request.user, qs)



    qs = qs[:5]

    #warcraftlogs
    logs_list = WarcraftlogsAPI.objects.all().order_by('-end')
    logs_list = logs_list[:5]

    #wowtoken
    wow_token = WowTokenApi.objects.all()

    #chatterbox
    chatterbox = Chatterbox.objects.all().order_by('-pub_date')
    chatterbox = chatterbox[:5:-1]

    #article comments
    comment_count = {}
    try:
        comments = ArticleComment.objects.all()
    except:
        comments = []

    for article in article_list:
        comment_count[article.id] = 0

    for comment in comments:
        if comment.origin_id in comment_count:
            comment_count[comment.origin_id] += 1
        else:
            comment_count[comment.origin_id] = 1

    if "chatterbox_form" in request.POST:
        form = ChatterboxForm(request.POST, request.FILES)
        if form.is_valid():
            #form.save()
            instance = form.save(commit=False)
            instance.author = request.user
            instance.pub_date = timezone.now()
            instance.save()
            return HttpResponseRedirect('/')
    else:
        form = ChatterboxForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['user'] = user
    args['chatterbox'] = chatterbox
    args['newsArticles'] = articles
    args['recruitment'] = recruitment_list
    args['group'] = group_name
    args['topic_list'] = qs
    args['logs_list'] = logs_list
    args['wow_token'] = wow_token
    args['comment_count'] = comment_count
    args['recruits'] = recruits

    return render_to_response('home/index.html', args, context_instance=RequestContext(request))


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
    # sort_by = request.GET.get('order_by', '-pub_date')
    # if sort_by not in ['-pub_date', 'pub_date', '-author', 'author']:
    #     sort_by = '-pub_date'
    # article_list = NewsArticle.objects.order_by(sort_by)
    #
    # VALID_SORTS = {
    #    "pk": "pk",
    #     "pkd": "-pk",
    #    "em": "eminence",
    #    "emd": "-eminence",
    #}
    #DEFAULT_SORT = 'pk'
    #def search(request):
    #    sort_key = request.GET.get('sort', DEFAULT_SORT) # Replace pk with your default.
    #    sort = VALID_SORTS.get(sort_key, DEFAULT_SORT)

    #    eList = Employer.objects.filter(eminence__lt=4).order_by(sort)

    #search
    ##article_list = NewsArticle.objects.filter(title__contains='a')

    article_list = NewsArticle.objects.all().order_by('-pub_date')
    paginator = Paginator(article_list, 5)

    page = request.GET.get('page')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    #article comments
    comment_count = {}
    try:
        comments = ArticleComment.objects.all()
    except:
        comments = []

    for article in article_list:
        comment_count[article.id] = 0

    for comment in comments:
        if comment.origin_id in comment_count:
            comment_count[comment.origin_id] += 1
        else:
            comment_count[comment.origin_id] = 1

    return render_to_response('home/news_articles.html',
                             {'newsArticles': articles,
                              'user': user,
                              'group': group_name,
                              'comment_count': comment_count},
                               context_instance=RequestContext(request))


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

    #edit article form
    instance = get_object_or_404(NewsArticle, id=article_id)
    form = NewsArticleForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/articles/all')

    #get comments
    try:
        comments = ArticleComment.objects.all().filter(origin=article_id).order_by('pub_date')
        comment_number = comments.count()
    except:
        comments = None
        comment_number = 0

    #comment form
    if "comment_form" in request.POST:
        form_comments = CommentForm(request.POST, request.FILES)
        if form_comments.is_valid():
            article_c = get_object_or_404(NewsArticle, id=article_id)
            instance = form_comments.save(commit=False)
            instance.author = request.user
            instance.pub_date = timezone.now()
            instance.origin = article_c
            instance.save()
            return HttpResponseRedirect('/articles/get/%s' % article_id)
    else:
        form_comments = CommentForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['form_comments'] = form_comments
    args['user'] = user
    args['group'] = group_name
    args['newsArticle'] = article
    args['comments'] = comments
    args['comment_number'] = comment_number

    return render_to_response('home/news_article.html', args, context_instance=RequestContext(request))


@permission_required('home.add_newsarticle', raise_exception=True)
def create(request):
    #if user is not logged in, forbidden
    user = None
    if request.user:
        user = request.user
    if user is None:
        raise PermissionDenied()

    #if the user is not an officer, forbidden
    #if not request.user.groups.filter(name='Officer'):
    #    raise PermissionDenied()

    if request.POST:
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            #form.save()
            instance = form.save(commit=False)
            instance.author = request.user
            instance.pub_date = timezone.now()
            #instance.body = bbcode.render_html(instance.body)
            #instance.body = mark_safe(instance.body.replace("\n", "<br/>"))
            instance.save()
            return HttpResponseRedirect('/articles/all')
    else:
        form = NewsArticleForm()
    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['user'] = user

    return render_to_response('home/create_news_article.html', args, context_instance=RequestContext(request))


def delete_article(request, article_id):
    #if user is not logged in, forbidden
    user = None
    if request.user:
        user = request.user
    if user is None:
        raise PermissionDenied()

    #group
    group_name = 'not_officer'
    if request.user.groups.filter(name='Officer'):
        group_name = 'Officer'

    try:
        article = NewsArticle.objects.get(id=article_id)
    except:
        raise Http404("Article does not exist")

    if request.user == article.author or group_name == 'Officer':
        instance = get_object_or_404(NewsArticle, id=article_id)
        form = DeleteNewsArticleForm(request.POST or None, instance=instance)
        if form.is_valid():
            article.delete()
            return HttpResponseRedirect('/articles/all')
    else:
        raise PermissionDenied()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['user'] = user
    args['newsArticle'] = article

    return render_to_response('home/delete_news_article.html', args, context_instance=RequestContext(request))


def like_article(request, article_id):
    if article_id:
        a = NewsArticle.objects.get(id=article_id)
        count = a.likes
        count += 1
        a.likes = count
        a.save()
    return HttpResponseRedirect('/articles/get/%s' % article_id)


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
                              'group': group_name},
                               context_instance=RequestContext(request))


def test_page(request):
    #recruitment_list = Recruitment.objects.all()
    if request.user:
        user = request.user
    else:
        user = None

    chatterbox = Chatterbox.objects.all().order_by('-pub_date')
    chatterbox = chatterbox[:5:-1]

    if "chatterbox_form" in request.POST:
        form = ChatterboxForm(request.POST, request.FILES)
        if form.is_valid():
            #form.save()
            instance = form.save(commit=False)
            instance.author = request.user
            instance.pub_date = timezone.now()
            instance.save()
            return HttpResponseRedirect('/articles/test')
    else:
        form = ChatterboxForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['user'] = user
    args['chatterbox'] = chatterbox

    return render_to_response('home/test_page.html', args, context_instance=RequestContext(request))


def delete_chatterbox(request, chat_id):
    #if user is not logged in, forbidden
    user = None
    if request.user:
        user = request.user
    if user is None:
        raise PermissionDenied()

    #group
    group_name = 'not_officer'
    if request.user.groups.filter(name='Officer'):
        group_name = 'Officer'

    try:
        chatterbox_chat = Chatterbox.objects.get(id=chat_id)
    except:
        raise Http404("Chat does not exist")

    if request.user == chatterbox_chat.author or group_name == 'Officer':
        instance = get_object_or_404(Chatterbox, id=chat_id)
        form = ChatterboxDeleteForm(request.POST or None, instance=instance)
        if form.is_valid():
            chatterbox_chat.delete()
            return HttpResponseRedirect('/')
    else:
        raise PermissionDenied()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['user'] = user
    args['chatterbox_chat'] = chatterbox_chat

    return render_to_response('home/delete_chatterbox.html', args, context_instance=RequestContext(request))


def delete_comment(request, comment_id):
    #if user is not logged in, forbidden
    user = None
    if request.user:
        user = request.user
    if user is None:
        raise PermissionDenied()

    #group
    group_name = 'not_officer'
    if request.user.groups.filter(name='Officer'):
        group_name = 'Officer'

    try:
        comment = ArticleComment.objects.get(id=comment_id)
    except:
        raise Http404("Comment does not exist")

    if request.user == comment.author or group_name == 'Officer':
        instance = get_object_or_404(ArticleComment, id=comment_id)
        form = DeleteCommentForm(request.POST or None, instance=instance)
        if form.is_valid():
            comment.delete()
            return HttpResponseRedirect('/')
    else:
        raise PermissionDenied()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['user'] = user
    args['comment'] = comment

    return render_to_response('home/delete_comment.html', args, context_instance=RequestContext(request))


def roster(request):
    #group
    group_name = 'not_officer'
    if request.user.groups.filter(name='Officer'):
        group_name = 'Officer'

    #get list of members
    valid_sorts = {
        "n": "name",
        "-n": "-name",
        "l": "level",
        "-l": "-level",
        "s": "spec",
        "-s": "-spec",
        "c": "player_class_string",
        "-c": "-player_class_string",
        "r": "rank",
        "-r": "-rank",
        "u": "timestamp",
        "-u": "-timestamp",
    }
    default_sort = 'name'
    sort_key = request.GET.get('sort', default_sort)
    sort = valid_sorts.get(sort_key, default_sort)

    members = Member.objects.all().order_by(sort)
    #members = Member.objects.all().order_by('name')

    return render_to_response('home/roster.html', {'members': members,
                                                   'group': group_name}, context_instance=RequestContext(request))