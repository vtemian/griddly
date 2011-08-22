from django import forms


class UserLogin(forms.Form):
    email = forms.EmailField(max_length=30)
    password = forms.PasswordInput()

    def get_user(self):
        return authenticate