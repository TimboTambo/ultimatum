from urllib2 import urlopen, URLError

from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.utils.http import urlencode

from users.models import SiteUser
from users.forms import FriendSelectForm


# Create your views here.
def add_friends(request):
    args = {}
    this_user = request.user.siteuser
    if request.method == 'POST':
        form = FriendSelectForm(request.POST)
        if form.is_valid():
            this_user.friends.clear()
            for user in form.cleaned_data['friends']:
                request.user.siteuser.friends.add(user)
            return HttpResponseRedirect('/accounts/register_success')
        else:
            args["error"] = "The information you entered was not valid. Please try again."
            args["form"] = form
    else:
        args['form'] = FriendSelectForm(user=this_user, initial={"friends":this_user.friends.all()})
    args.update(csrf(request))
    return render_to_response('users/add_friends.html', args)