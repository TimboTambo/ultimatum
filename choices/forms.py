import datetime
from django import forms
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Textarea
from choices.models import Choice
from django.utils.translation import ugettext_lazy as _


class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'option1', 'option2', 'time_limit']
        widgets = {
        }
        labels = {
            'question': _('Question'),
            'option1': _('Option A'),
            'option2': _('Option B'),
            'time_limit': _('Time Limit'),
        }
        help_texts = {
            #'question': _('Enter your question.'),
        }
        error_messages = {
            #'title': {
            #    'max_length': _("This writer's name is too long."),
            #},
        }
