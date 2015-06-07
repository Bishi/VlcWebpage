from pybb.permissions import DefaultPermissionHandler
from django.db.models import Q
from pybb import defaults


class MyPermissionHandler(DefaultPermissionHandler):

    def filter_categories(self, user, qs):
        new_qs = qs

        if not user.is_staff:
            new_qs = qs.filter(hidden=False)
        if user.is_staff:
            if user.groups.filter(name='Officer'):
                new_qs = qs
            else:
                new_qs = qs.exclude(name='Officer')

        return new_qs

    def filter_forums(self, user, qs):
        """ return a queryset with forums `user` is allowed to see """
        return qs.filter(Q(hidden=False) & Q(category__hidden=False)) if not user.is_staff else qs

    def may_view_category(self, user, category):
        """ return True if `user` may view this category, False if not """
        tmp = False
        if user.is_staff or not category.hidden:
            tmp = True
        if category.id == 5 and not user.groups.filter(name='Officer'):
            tmp = False

        return tmp

    def may_view_forum(self, user, forum):
        """ return True if user may view this forum, False if not """
        # return False
        tmp = False
        if user.is_staff:
            tmp = True
        elif forum.hidden == False and forum.category.hidden == False:
            tmp = True
        if forum.category.name == 'Officer' and not user.groups.filter(name='Officer'):
            tmp = False

        return tmp

    def may_view_topic(self, user, topic):
        """ return True if user may view this topic, False otherwise """
        if user.is_superuser:
            return True
        if not user.is_staff and (topic.forum.hidden or topic.forum.category.hidden):
            return False  # only staff may see hidden forum / category
        if topic.on_moderation:
            return user.is_authenticated() and (user == topic.user or user in topic.forum.moderators)
        if topic.forum.category.name == 'Officer' and not user.groups.filter(name='Officer'):
            return False
        return True

    def filter_topics(self, user, qs):
        """ return a queryset with topics `user` is allowed to see """
        if not user.is_staff:
            qs = qs.filter(Q(forum__hidden=False) & Q(forum__category__hidden=False))
        if not user.is_superuser:
            if user.is_authenticated():
                qs = qs.filter(Q(forum__moderators=user) | Q(user=user) | Q(on_moderation=False)).distinct()
            else:
                qs = qs.filter(on_moderation=False)
        if not user.groups.filter(name='Officer'):
            qs = qs.exclude(Q(forum__category__name='Officer'))

        return qs

    def may_create_topic(self, user, forum):
        """ return True if `user` is allowed to create a new topic in `forum` """
        return user.has_perm('pybb.add_post')

    def may_view_post(self, user, post):
        """ return True if `user` may view `post`, False otherwise """
        if user.is_superuser:
            return True
        if post.on_moderation:
            return post.user == user or user in post.topic.forum.moderators.all()
        if post.topic.forum.category.name == 'Officer' and not user.groups.filter(name='Officer'):
            return False
        return True

    def filter_posts(self, user, qs):
        """ return a queryset with posts `user` is allowed to see """

        # first filter by topic availability
        if not user.is_staff:
            qs = qs.filter(Q(topic__forum__hidden=False) & Q(topic__forum__category__hidden=False))

        if not defaults.PYBB_PREMODERATION or user.is_superuser:
            # superuser may see all posts, also if premoderation is turned off moderation
            # flag is ignored
            if not user.groups.filter(name='Officer'):
                qs = qs.exclude(Q(topic__forum__category__name='Officer'))
            return qs
        elif user.is_authenticated():
            # post is visible if user is author, post is not on moderation, or user is moderator
            # for this forum
            qs = qs.filter(Q(user=user) | Q(on_moderation=False) | Q(topic__forum__moderators=user))
        else:
            # anonymous user may not see posts which are on moderation
            qs = qs.filter(on_moderation=False)

        return qs