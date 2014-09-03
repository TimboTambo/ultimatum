from urllib2 import urlopen, URLError

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.utils.http import urlencode

from ultimatum.forms import LoginForm, RegistrationForm
from users.models import SiteUser
#from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser


def splash(request):
    return redirect("/welcome/", permanent=True)

def welcome(request):
    return render_to_response("login/welcome.html")

def login(request):
    error = None
    username = ''
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/accounts/loggedin')
        else:
            error = "Username or password is incorrect"
    c = {"error": error, "username": username}
    c.update(csrf(request))
    return render_to_response('login/login.html', c)


@login_required
def home(request, message=None):
    if message:
        message = message.replace("User", request.user.username.title())
    return render_to_response('home.html',
                              {"message": message})


def logout(request):
    auth.logout(request)
    return render_to_response('login/logout.html')


def register_user(request):
    # Has any info been posted through? 1st time loaded, not. 2nd time yes
    error = None
    args = {}

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            SiteUser.objects.create(user=new_user)
            username = request.POST.get('username', '')
            password = request.POST.get('password1', '')
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return HttpResponseRedirect('/accounts/register_success')
        else:
            args["error"] = "The information you entered was not valid. Please try again."
            args["form"] = form
    else:
        args['form'] = RegistrationForm()

    args.update(csrf(request))
    return render_to_response('login/register.html', args)


def register_success(request):
    return render_to_response('login/register_success.html')
