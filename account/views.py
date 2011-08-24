from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from account.form import UserRegister, UserLogin

from account.models import UserProfile

def register(request):
    if request.method == "POST":
        form =  UserRegister(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'])
            user.save()
            UserProfile(user=user).save()
            auth_login(request,authenticate(username=request.POST['username'], password=request.POST['password']))
            return redirect('/game/')
        else:
            return HttpResponse('invalid form')

def login(request):
    form = UserLogin(request.POST)
    if form.is_valid():
        user = form.get_auth_user()
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponse('ok')
            return HttpResponse('disabled')
        return HttpResponse('not')
    else:
        return HttpResponse('error')
