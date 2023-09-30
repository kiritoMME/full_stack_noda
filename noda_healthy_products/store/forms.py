from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from User.models import User


class UserCreationForm(BaseUserCreationForm):
    mobile = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off','placeholder': 'رقم الهاتف'}))
    password1 = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete':'off','placeholder': 'إنشاء كلمة السر'}))
    password2 = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete':'off','placeholder': 'اعد كتابة كلمة السر'}))
    
    class Meta:
        model = User
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'الاسم الاول'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'اسم العائله'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'العنوان بالتفصيل'}),
        }

        fields = ('first_name', 'last_name', 'city', 'address', 'mobile', 'password1', 'password2')

class LoginForm(forms.Form):
    mobile = forms.CharField(max_length=20, required=True, help_text='Phone number')
    password = forms.CharField()
    

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')
