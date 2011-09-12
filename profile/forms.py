from django.contrib.auth.models import User
from django import forms

class UserChangePassword(forms.Form):
    old_password = forms.CharField(max_length=50)
    new_password = forms.CharField(max_length=50)

class UserChangeEmail(forms.Form):
    email = forms.EmailField(max_length=50)

    def clean(self):
        data = self.cleaned_data
        email = data.get('email')
        user = User.objects.filter(email=email).exists()
        if user:
            raise forms.ValidationError('This email is in the database')
        return data
class UserChangeFirstName(forms.Form):
    first_name = forms.CharField(max_length=50)

class UserChangeLastName(forms.Form):
    last_name = forms.CharField(max_length=50)

class UserChangePersonalInfo(forms.Form):
    info = forms.CharField(max_length=50)