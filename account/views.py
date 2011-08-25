from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from account.form import UserRegister

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
    user = authenticate(username='secret', password='secret')
    if user is not None:
        if user.is_active:
            auth_login(request, user)
        else:
            print "Your account has been disabled!"
    else:
        print "Your username and password were incorrect."
