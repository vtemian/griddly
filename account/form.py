from django import forms
from django.contrib.auth import authenticate


class UserRegister(forms.Form):
    email = forms.EmailField(max_length=30)
    password = forms.PasswordInput()
    username = forms.CharField(max_length=30)

class UserLogin(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)

    def get_auth_user(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
