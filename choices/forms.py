from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from choices.models import Choice, Comment


class ChoiceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ChoiceForm, self).__init__(*args, **kwargs)
        if user:
            print "User friends:", user.friends.all()
            self.fields['share_list'].queryset = user.friends.all() 

    class Meta:
        model = Choice
        fields = ['question', 'image1', 'image2', 'text1', 'text2', 'url1', 'url2', 
                  'time_limit', 'share_with', 'share_list']
        widgets = {
            'share_list': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'question': _('Question'),
            'image1': _('Image'),
            'text1': _('Text'),
            'url1': _('URL'),
            'image2': _('Image'),
            'text2': _('Text'),
            'url2': _('URL'),
            'time_limit': _('Time limit'),
            'share_with': _('Share with'),
        }

    def clean(self, *args, **kwargs):
        super(ChoiceForm, self).clean(*args, **kwargs)
        image1 = self.cleaned_data["image1"]
        text1 = self.cleaned_data["text1"]
        url1 = self.cleaned_data["url1"]

        if not (image1 or text1 or url1):
            raise forms.ValidationError("Please enter something for Option A")

        image2 = self.cleaned_data.get("image2")
        text2 = self.cleaned_data.get("text2")
        url2 = self.cleaned_data.get("url2")

        if not (image2 or text2 or url2):
            raise forms.ValidationError("Please enter something for Option B")

        if self.cleaned_data["share_with"] == "public":
            self.cleaned_data["share_list"] == []
        return self.cleaned_data

class VoteForm(forms.Form):
    vote = forms.ChoiceField(choices=((1, "Option A"), (2, "Option B")))


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':2, 'cols':20}),
        }

class AcceptedForm(forms.Form):
    accepted = forms.ChoiceField(choices=(("A", "Option A"), ("B", "Option B")))