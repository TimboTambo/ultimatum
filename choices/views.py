from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.db.models import F, Q
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Context
from django.template.loader import get_template

from choices.models import Choice, Comment
from choices.forms import ChoiceForm, VoteForm, CommentForm


@login_required
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
            # m2m needs to be saved manually after a partial save of instance:
            # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method
            form.save_m2m()
            return HttpResponseRedirect('/choices/submitted/')
        else:
            args['form'] = form
    else:
        args['form'] = ChoiceForm(user=this_user, initial={"share_list": this_user.friends.all()})
    args.update(csrf(request))
    return render_to_response('choices/create_choice.html', args)


@login_required
def submitted(request):
    args = {'choice':Choice.objects.filter(created_by=request.user).reverse()[0]}
    return render_to_response('choices/submitted_choice.html', args)


@login_required
def view_ultimatums(request):
    args = {}
    this_user = request.user.siteuser
    args['user_ultimatums'] = sorted(Choice.objects.filter(created_by=this_user), key=sort)
    args['other_ultimatums'] = sorted(Choice.objects.filter(share_list=this_user), key=sort)
    args['public_ultimatums'] = sorted(Choice.objects.filter(share_with="public").exclude(created_by=this_user), key=sort)
    return render_to_response('choices/view_ultimatums.html', args)


def sort(m):
    if m.time_remaining < 0:
        return 100000
    return m.time_remaining


@login_required
def view_ultimatum(request, id=None):
    args = {}
    this_user = request.user.siteuser
    this_choice = get_object_or_404(Choice, pk=id)
    args['choice'] = this_choice

    if (request.method == 'POST' and this_user not in this_choice.voted_1.all()
        and this_user not in this_choice.voted_2.all()):
        form = VoteForm(request.POST)
        form2 = CommentForm(request.POST)
        if form.is_valid():
            vote = int(form.cleaned_data['vote'])
            if vote==1:
                this_choice.voted_1.add(this_user)
            elif vote==2:
                this_choice.voted_2.add(this_user)
            this_choice.save()
            if form2.is_valid():
                content = form2.cleaned_data['content']
                if content:
                    Comment.objects.create(user=this_user, choice=this_choice, content=content) 
            args["message"] = "Thank you for voting."
            return render_to_response('choices/view_ultimatum.html', args)

    if this_choice.expired:
        args['votes_1'] = len(this_choice.voted_1.all())
        args['votes_2'] = len(this_choice.voted_2.all())
        args['total_votes'] = args['votes_1'] + args['votes_2']
        args['commentsA'] = this_choice.comment_set.filter(choice__voted_1 = F('user'))
        args['commentsB'] = this_choice.comment_set.filter(choice__voted_2 = F('user'))
        return render_to_response('choices/view_ultimatum_results.html', args)

    if not (this_choice.created_by==this_user):
        if (this_user in this_choice.share_list.all()):
            if (this_user not in this_choice.voted_1.all() and 
                this_user not in this_choice.voted_2.all()):
                args['form'] = VoteForm()
                args['form2'] = CommentForm()
                args.update(csrf(request))
                args["message"] = "You have not yet voted."
            else:
                args["message"] = "You have already voted"
    
    else:
        args["message"] = "Please come back later to review the results of your question."


    args.update(csrf(request))
    return render_to_response('choices/view_ultimatum.html', args)    