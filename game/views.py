from django.shortcuts import render_to_response, redirect, render
from django.template.context import RequestContext
from account.models import UserProfile

def start(request):
    return render_to_response('game.html',
                          {'userprofile' : UserProfile.objects.get(user=request.user)},
                          context_instance=RequestContext(request))

