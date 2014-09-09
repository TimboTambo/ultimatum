from django import forms
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long")
        elif password1.lower() == password1:
            raise forms.ValidationError("Password must contain at least one uppercase character")
        elif password1.isalpha():
            raise forms.ValidationError("Password must contain at least one number of symbol")
        return password1


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)