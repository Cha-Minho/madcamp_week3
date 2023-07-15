from django import forms
from .models import User

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        exclude = ['created_at', 'updated_at']
        fields = ('username', 'password', 'email')
        widget = {
            'password': forms.PasswordInput
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)