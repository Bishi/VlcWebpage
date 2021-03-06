from django.utils import timezone
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, JsonResponse, QueryDict
from home.forms import NewsArticleForm, DeleteNewsArticleForm, ChatterboxForm, CommentForm
from home.models import NewsArticle, WarcraftlogsAPI, WowTokenApi, Chatterbox
from home.models import ArticleComment, Member, Recruit, RaidProgress, RaidBoss
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from pybb.permissions import perms
from django.shortcuts import get_object_or_404
from pybb.models import Topic
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse


def is_officer(request):
    if request.user.groups.filter(name='Officer'):
        return True
    else:
        return False


#homepage
def index_view(request):
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

    #recruit
    recruits = Recruit.objects.all().order_by('name_text')
    #order by if recruits are needed
    tmp = []
    for recruit in recruits:
        if recruit.spec1.is_needed or recruit.spec2.is_needed or recruit.spec3.is_needed:
            tmp.append(recruit)
    for recruit in recruits:
        if not recruit.spec1.is_needed and not recruit.spec2.is_needed and not recruit.spec3.is_needed:
            tmp.append(recruit)

    recruits = tmp

    #latest forum posts
    topic_list = Topic.objects.all().select_related().order_by('-updated', '-id')
    topic_list = perms.filter_topics(request.user, topic_list)
    topic_list = topic_list[:5]

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
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ChatterboxForm()

    #raid progress
    raid_progress = RaidProgress.objects.all().order_by('order')
    raid_bosses = RaidBoss.objects.all()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['chatterbox'] = chatterbox
    args['newsArticles'] = articles
    args['topic_list'] = topic_list
    args['logs_list'] = logs_list
    args['wow_token'] = wow_token
    args['comment_count'] = comment_count
    args['recruits'] = recruits
    args['raid_progress'] = raid_progress
    args['raid_bosses'] = raid_bosses

    return render_to_response('home/index.html', args, context_instance=RequestContext(request))


def home_redirect(response):
    return HttpResponseRedirect(reverse('home'))


#/home/all
def news_articles(request):
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

    args = {'newsArticles': articles, 'comment_count': comment_count}

    return render_to_response('home/news_articles.html', args, context_instance=RequestContext(request))


def news_article(request, article_id=1):
    try:
        article = NewsArticle.objects.get(id=article_id)
    except:
        raise Http404("Article does not exist")

    #edit article form
    instance = get_object_or_404(NewsArticle, id=article_id)
    if "edit_article_form" in request.POST:
        form = NewsArticleForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home:articles'))
    else:
        form = NewsArticleForm(request.POST or None, instance=instance)
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
            return HttpResponseRedirect(reverse('home:article', args=(article_id,)))
    else:
        form_comments = CommentForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['form_comments'] = form_comments
    args['newsArticle'] = article
    args['comments'] = comments
    args['comment_number'] = comment_number

    return render_to_response('home/news_article.html', args, context_instance=RequestContext(request))


@permission_required('home.add_newsarticle', raise_exception=True)
def create(request):
    if request.POST:
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            #form.save()
            instance = form.save(commit=False)
            instance.author = request.user
            instance.pub_date = timezone.now()
            instance.save()
            return HttpResponseRedirect(reverse('home:articles'))
    else:
        form = NewsArticleForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('home/create_news_article.html', args, context_instance=RequestContext(request))


@login_required
def delete_article(request, article_id):
    try:
        article = NewsArticle.objects.get(id=article_id)
    except:
        raise Http404("Article does not exist")

    # can delete the article if user is the author or if user is in the Officer group
    if request.user == article.author or is_officer(request):
        instance = get_object_or_404(NewsArticle, id=article_id)
        form = DeleteNewsArticleForm(request.POST or None, instance=instance)
        if form.is_valid():
            article.delete()
            return HttpResponseRedirect(reverse('home:articles'))
    else:
        raise PermissionDenied()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['newsArticle'] = article

    return render_to_response('home/delete_news_article.html', args, context_instance=RequestContext(request))


def application_info(request):
    return render_to_response('home/application_info.html', context_instance=RequestContext(request))


def test_page(request):
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
            return HttpResponseRedirect(reverse('home:test'))
    else:
        form = ChatterboxForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['chatterbox'] = chatterbox

    return render_to_response('home/test_page.html', args, context_instance=RequestContext(request))


def roster(request):
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
        "il": "item_level",
        "-il": "-item_level"
    }
    default_sort = 'name'
    sort_key = request.GET.get('sort', default_sort)
    sort = valid_sorts.get(sort_key, default_sort)

    members = []

    if sort_key != 'il' and sort_key != '-il':
        members = Member.objects.all().order_by(sort)
    elif sort_key == 'il':
        # members = Member.objects.extra(select={'tmp': 'CAST(-item_level AS INTEGER)'}).order_by('tmp')
        members = Member.objects.extra(select={'tmp': "case when item_level != 'Unknown' then "
                                                      "to_number(item_level, '999') else 0 end"}).order_by('-tmp')
    elif sort_key == '-il':
        # members = Member.objects.extra(select={'tmp': 'CAST(item_level AS INTEGER)'}).order_by('tmp')
        members = Member.objects.extra(select={'tmp': "case when item_level != 'Unknown' then "
                                                      "to_number(item_level, '999') else 0 end"}).order_by('tmp')

    #members = Member.objects.extra(select={'tmp': 'CAST(item_level AS INTEGER)'}).order_by('tmp')

    args = {'members': members}

    return render_to_response('home/roster.html', args, context_instance=RequestContext(request))


@login_required
def chatterbox_archive(request):
    chat = Chatterbox.objects.all().order_by('-pub_date')

    paginator = Paginator(chat, 25, 5)
    page = request.GET.get('page')
    try:
        chat = paginator.page(page)
    except PageNotAnInteger:
        chat = paginator.page(1)
    except EmptyPage:
        chat = paginator.page(paginator.num_pages)

    args = {'chatterbox': chat}

    return render_to_response('home/chat_archive.html', args, context_instance=RequestContext(request))


@login_required
def delete_chat(request):
    """
    Ajax script delete_chat does the work
    """
    if request.method == 'DELETE':
        post = Chatterbox.objects.get(pk=int(QueryDict(request.body).get('postpk')))

        # can delete the comment if user is the author or if user is in the Officer group
        if is_officer(request) or request.user == post.author:
            post.delete()

            response_data = {}
            response_data.update(csrf(request))
            response_data = {'message': 'Post was deleted.'}

            return JsonResponse(response_data)
        else:
            raise PermissionDenied()

    else:
        return JsonResponse({'message': 'What are you even doing here?'})


@login_required
def delete_comment(request):
    """
    Ajax script delete_comment does the work
    """
    if request.method == 'DELETE':
        post = ArticleComment.objects.get(pk=int(QueryDict(request.body).get('postpk')))

        # can delete the comment if user is the author or if user is in the Officer group
        if is_officer(request) or request.user == post.author:
            post.delete()

            response_data = {}
            response_data.update(csrf(request))
            response_data = {'message': 'Post was deleted.'}

            return JsonResponse(response_data)
        else:
            raise PermissionDenied()

    else:
        return JsonResponse({'message': 'What are you even doing here?'})
