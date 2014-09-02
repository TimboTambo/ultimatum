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

from choices.models import Choice
from choices.forms import ChoiceForm

def create_choice(request):
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        form = ChoiceForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            choice = form.save(commit=False)
            choice.created_by = request.user
            choice.time_created = timezone.now()
            choice.save()
            return HttpResponseRedirect('/choices/submitted/')
        else:
            args['form'] = form
    else:
        args['form'] = ChoiceForm()

    return render_to_response('choices/create_choice.html', args)


def submitted(request):
    args = {'choice':Choice.objects.filter(created_by=request.user).reverse()[0]}
    return render_to_response('choices/submitted_choice.html', args)