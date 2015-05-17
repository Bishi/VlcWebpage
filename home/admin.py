from django.contrib import admin
from home.models import NewsArticle, Recruitment, ClassName, ClassRole, WarcraftlogsAPI, WarcraftlogsURL, RealmStatusAPI
from home.models import ArticleComment
from home.models import Chatterbox
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _


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


admin.site.register(ClassName, ClassNameAdmin)


class ClassRoleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Class Role',           {'fields': ['class_role_text']}),
    ]
    #list_display = ('class_role_text')


admin.site.register(ClassRole, ClassRoleAdmin)


class RecruitmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Class',               {'fields': ['class_name']}),
        ('Role',                {'fields': ['class_role']}),
    ]
    list_display = ('class_name', 'class_role')


admin.site.register(Recruitment, RecruitmentAdmin)


class WarcraftlogsAPIAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start')
    ordering = ('start',)


admin.site.register(WarcraftlogsAPI, WarcraftlogsAPIAdmin)


class WarcraftlogsUrlAdmin(admin.ModelAdmin):
    pass


admin.site.register(WarcraftlogsURL, WarcraftlogsUrlAdmin)


class RealmStatusAPIAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')


admin.site.register(RealmStatusAPI, RealmStatusAPIAdmin)


class ChatterboxAdmin(admin.ModelAdmin):
    list_display = ('body', 'author')

admin.site.register(Chatterbox, ChatterboxAdmin)


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'origin', 'body')

admin.site.register(ArticleComment, ArticleCommentAdmin)


#custom user admin, only superusers can change 'is superuser' status
class MyUserAdmin(UserAdmin):
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        else:
            # modify these to suit the fields you want your
            # staff user to be able to edit
            perm_fields = ('is_active', 'is_staff', 'groups')

        return [(None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                (_('Permissions'), {'fields': perm_fields}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')})]

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)