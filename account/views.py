from django.http import HttpResponse
from django.contrib.auth.models import User, check_password
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect, render, render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from account.form import UserRegister, UserLogin, UserChangePassword

from account.models import UserProfile

def profile(request):
    user = UserProfile.objects.get(user=request.user)
    return render_to_response('my_profile.html',
                              {'userprofile' : user},
                              context_instance=RequestContext(request))

def register(request):
    if request.method == "POST":
        form =  UserRegister(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'])
            user.save()
            UserProfile(user=user).save()
            auth_login(request,authenticate(username=request.POST['username'], password=request.POST['password']))
            return HttpResponse(simplejson.dumps({'ok': '/game'}))
        else:
            return HttpResponse(simplejson.dumps(form.errors))

def login(request):
    form = UserLogin(request.POST)
    if form.is_valid():
        user = form.get_auth_user()
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponse(simplejson.dumps({'ok': '/game'}))
            return HttpResponse(simplejson.dumps({'disabled': 'This account has been disabled'}))
        return HttpResponse(simplejson.dumps({'not': 'Incorect username or password'}))
    else:
        return HttpResponse(simplejson.dumps(form.errors))

def password_change(request):
    if request.method == 'POST':
        form = UserChangePassword(request.POST)
        if form.is_valid():
            print request.POST.get('new_password')
            if check_password(request.POST.get('old_password'), request.user.password):
                user = request.user
                user.set_password(request.POST.get('new_password'))
                user.save()
                return HttpResponse(simplejson.dumps({'message': 'The password has been changed'}))
            else:
                 return HttpResponse(simplejson.dumps({'lol': 'Incorect password'}))
        else:
            return HttpResponse(simplejson.dumps(form.errors))
    return redirect('/game')

s


