from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from choices.models import Choice, Comment


class ChoiceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ChoiceForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['share_list'].queryset = user.friends.all() 

    class Meta:
        model = Choice
        fields = ['question', 'option1', 'option2', 'time_limit', 'share_with', 'share_list']
        widgets = {
            'share_list': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'question': _('Question'),
            'option1': _('Option A'),
            'option2': _('Option B'),
            'time_limit': _('Time Limit'),
        }


class VoteForm(forms.Form):
    vote = forms.ChoiceField(choices=((1, "Option A"), (2, "Option B")))


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':2, 'cols':20}),
        }