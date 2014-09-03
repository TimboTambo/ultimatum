from django import forms
from django.forms import ModelForm
from users.models import SiteUser
from django.utils.translation import ugettext_lazy as _


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

