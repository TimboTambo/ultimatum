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
from choices.forms import ChoiceForm, VoteForm

def create_choice(request):
    args = {}
    this_user = request.user.siteuser
    if request.method == 'POST':
        form = ChoiceForm(request.POST, request.FILES)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.created_by = this_user
            choice.time_created = timezone.now()
            choice.save()
            # m2m needs to be saved manually:
            #https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method
            form.save_m2m()
            return HttpResponseRedirect('/choices/submitted/')
        else:
            args['form'] = form
    else:
        args['form'] = ChoiceForm(user=this_user, initial={"share_list": this_user.friends.all()})
    args.update(csrf(request))
    return render_to_response('choices/create_choice.html', args)


def submitted(request):
    args = {'choice':Choice.objects.filter(created_by=request.user).reverse()[0]}
    return render_to_response('choices/submitted_choice.html', args)


def view_ultimatums(request):
    args = {}
    this_user = request.user.siteuser
    args['user_ultimatums'] = Choice.objects.filter(created_by=this_user)
    args['other_ultimatums'] = Choice.objects.filter(share_list=this_user)
    return render_to_response('choices/view_ultimatums.html', args)

def view_ultimatum(request, id=None):
    args = {}
    this_user = request.user.siteuser
    this_choice = get_object_or_404(Choice, pk=id)

    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            vote = int(form.cleaned_data['vote'])
            if vote==1:
                this_choice.voted_1.add(this_user)
            elif vote==2:
                this_choice.voted_2.add(this_user)
            this_choice.save()    
            args["message"] = "Thank you for voting."
            return render_to_response('choices/view_ultimatum.html', args)

    args['choice'] = this_choice

    if this_choice.expired:
        args['votes_1'] = len(this_choice.voted_1.all())
        args['votes_2'] = len(this_choice.voted_2.all())
        return render_to_response('choices/view_ultimatum_results.html', args)

    if not (this_choice.created_by==this_user):
        if (this_user in this_choice.share_list.all()):
            if (this_user not in this_choice.voted_1.all() and 
                this_user not in this_choice.voted_2.all()):
                args['form'] = VoteForm()
                args.update(csrf(request))
                args["message"] = "You have not yet voted."
            else:
                args["message"] = "You have already voted"
        
    else:
        args["message"] = "Please come back later to review the results of your question."

    return render_to_response('choices/view_ultimatum.html', args)    