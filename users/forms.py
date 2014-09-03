import datetime
from django import forms
from django.forms import ModelForm, Textarea
from users.models import SiteUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple


class FriendSelectForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FriendSelectForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['friends'].queryset = SiteUser.objects.exclude(pk=user.pk)    

    class Meta:
        model = SiteUser
        fields = ['friends']
        widgets = {
            'friends': forms.CheckboxSelectMultiple(),
        }
        labels = {
         
         }
        help_texts = {
            #'question': _('Enter your question.'),
        }
        error_messages = {
            #'title': {
            #    'max_length': _("This writer's name is too long."),
            #},
        }

