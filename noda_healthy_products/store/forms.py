from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from User.models import User


class UserCreationForm(BaseUserCreationForm):
    mobile = forms.CharField(max_length=20, required=True, help_text='Phone number')
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'mobile', 'password1', 'password2')

class LoginForm(forms.Form):
    mobile = forms.CharField(max_length=20, required=True, help_text='Phone number')
    password = forms.CharField(widget=forms.PasswordInput)
    

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')
