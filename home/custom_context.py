from home.models import RealmStatusAPI
from django.contrib.auth import views as auth_view
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from account.conf import settings
from account.forms import LoginUsernameFormBase


#realm status api
def home_context(request):
    realm_status = RealmStatusAPI.objects.all()
    group_name = 'not_officer'
    if request.user.groups.filter(name='Officer'):
        group_name = 'Officer'

    #login form
    if "login_form" in request.POST:
        login_form = LoginUsernameFormBase(request.POST)
        if login_form.is_valid():
            auth_view.login(request, login_form.user)
            expiry = settings.ACCOUNT_REMEMBER_ME_EXPIRY if login_form.cleaned_data.get("remember") else 0
            request.session.set_expiry(expiry)
            return HttpResponseRedirect('/')
    else:
        login_form = LoginUsernameFormBase()

    args = {}
    args.update(csrf(request))

    args['realm_status'] = realm_status
    args['group'] = group_name
    args['login_form'] = login_form
    return args