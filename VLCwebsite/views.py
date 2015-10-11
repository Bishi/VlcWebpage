from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from  django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
import VLCwebsite.forms
from django.template import RequestContext
from django.shortcuts import render_to_response


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404

    return response


def handler403(request):
    response = render_to_response('403.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 403

    return response
