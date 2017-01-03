from django.contrib import admin
from home.models import NewsArticle, WarcraftlogsAPI, WarcraftlogsURL, RealmStatusAPI
from home.models import ArticleComment, WowTokenApi, Member, Spec, Recruit, RaidProgress, RaidBoss
from home.models import Chatterbox
from home.models import EndpointUrl
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class NewsArticleAdmin(admin.ModelAdmin):
    #when we click on the artickle
    fieldsets = [
        (None,                  {'fields': ['title']}),
        ('Date information',    {'fields': ['pub_date']}),
        ('Body',                {'fields': ['body']}),
        ('Body_html',           {'fields': ['body_html']}),
        ('Img',                 {'fields': ['thumbnail']}),
        ('Author',              {'fields': ['author']}),
        #(('Additional options'), {
        #        'classes': ('collapse',),
        #        'fields': ('body_html',)
        #        }
        # ),
    ]
    #inlines = [ChoiceInLine]

    #displays al the articles with these
    list_display = ('title', 'pub_date', 'author')


admin.site.register(NewsArticle, NewsArticleAdmin)


class ClassNameAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Class Name',           {'fields': ['class_name_text']}),
        ('Img',                  {'fields': ['pic']}),
    ]
    #list_display = ('class_name_text','pic')


#admin.site.register(ClassName, ClassNameAdmin)


class ClassRoleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Class Role',           {'fields': ['class_role_text']}),
    ]
    #list_display = ('class_role_text')


#admin.site.register(ClassRole, ClassRoleAdmin)


class RecruitmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Class',               {'fields': ['class_name']}),
        ('Role',                {'fields': ['class_role']}),
    ]
    list_display = ('class_name', 'class_role')


#admin.site.register(Recruitment, RecruitmentAdmin)


class SpecAdmin(admin.ModelAdmin):
    list_display = ('spec_name', 'is_needed')
    list_editable = ('is_needed',)


admin.site.register(Spec, SpecAdmin)


class RecruitAdmin(admin.ModelAdmin):
    pass


admin.site.register(Recruit, RecruitAdmin)


class WarcraftlogsAPIAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'start')
    ordering = ('start',)


admin.site.register(WarcraftlogsAPI, WarcraftlogsAPIAdmin)


class WarcraftlogsUrlAdmin(admin.ModelAdmin):
    pass


admin.site.register(WarcraftlogsURL, WarcraftlogsUrlAdmin)


class EndpointUrlAdmin(admin.ModelAdmin):
    pass


admin.site.register(EndpointUrl, EndpointUrlAdmin)


class RealmStatusAPIAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')


admin.site.register(RealmStatusAPI, RealmStatusAPIAdmin)


class WowTokenApiAdmin(admin.ModelAdmin):
    pass

admin.site.register(WowTokenApi, WowTokenApiAdmin)


class ChatterboxAdmin(admin.ModelAdmin):
    list_display = ('body', 'author')

admin.site.register(Chatterbox, ChatterboxAdmin)


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'origin', 'body')

admin.site.register(ArticleComment, ArticleCommentAdmin)


class RaidBossInLine(admin.TabularInline):
    model = RaidBoss
    can_delete = False
    extra = 0


class RaidProgressAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'tier', '_get_defeated', 'bosses',)
    inlines = [RaidBossInLine]
    fieldsets = [('Raid Info',          {'fields': ['name', 'difficulty', 'tier', 'order', 'thumbnail']}), ]

    #child must be saved before the parent
    def save_model(self, request, obj, form, change):
        pass

    def save_formset(self, request, form, formset, change):
        formset.save()
        form.instance.save()

    def _get_defeated(self, obj):
        return obj.defeated_bosses
    _get_defeated.short_description = 'Defeated'

admin.site.register(RaidProgress, RaidProgressAdmin)


class RaidBossAdmin(admin.ModelAdmin):
    list_display = ('name', 'raid_instance', 'get_difficulty', 'defeated')
    list_editable = ('defeated',)

    def get_difficulty(self, obj):
        return obj.raid_instance.difficulty


admin.site.register(RaidBoss, RaidBossAdmin)


#custom user admin, only superusers can change 'is superuser' status
class MyUserAdmin(UserAdmin):
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        #superuser
        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        #staff
        else:
            # staff user to be able to edit
            perm_fields = ('is_active', 'is_staff', 'groups')

        return [(None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                (_('Permissions'), {'fields': perm_fields}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')})]

    list_filter = ['is_staff', 'is_superuser', 'groups', 'is_active', 'date_joined']
    list_display = ('username', 'is_staff', 'date_joined')

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


#roster
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank_string', 'player_class_string', 'spec', 'level', 'item_level', 'timestamp', 'pub_date')

admin.site.register(Member, MemberAdmin)
