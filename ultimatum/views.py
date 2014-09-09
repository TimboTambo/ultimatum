from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Context, RequestContext
from django.template.loader import get_template

from ultimatum.forms import LoginForm, RegistrationForm
from users.models import SiteUser


def splash(request):
    return redirect("/welcome/", permanent=True)

def welcome(request):
    return render_to_response("login/welcome.html")

def login(request):
    args={}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            print "User:",user
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/accounts/loggedin')
            elif not User.objects.filter(username=username):
                args["error"] = "Please enter a valid username or register as a new user"
            else:
                args["error"] = "Password incorrect"
        else:
            args["error"] = "Please enter both username and password"
        args["form"] = LoginForm(initial={"username": request.POST.get('username', '')})
    else:
        args["form"] = LoginForm()
    args.update(csrf(request))
    return render_to_response('login/login.html', args)

@login_required
def home(request, message=None):
    if message:
        message = message.replace("User", request.user.username.title())
    return render_to_response('home.html', {"message": message})

def logout(request):
    auth.logout(request)
    return render_to_response('login/logout.html')

def register_user(request):
    args = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            SiteUser.objects.create(user=new_user)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return HttpResponseRedirect('/users/update_friends')
        else:
            args["form"] = form
    else:
        args['form'] = RegistrationForm()
    args.update(csrf(request))
    return render_to_response('login/register.html', args)
