from django import forms


class UserRegister(forms.Form):
    email = forms.EmailField(max_length=30)
    password = forms.PasswordInput()
    username = forms.CharField(max_length=30)

class UserLogin(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)

    