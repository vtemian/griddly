from django.shortcuts import render_to_response, redirect, render
from django.template.context import RequestContext
from account.models import UserProfile
from profile.views import user_menu
from alliance.models import *
from territory.models import *


def start(request):
    context = user_menu(request)

    try:
        if context['userprofile'].clan_stream == 'news':
            context['news'] = AllianceNews.objects.filter(alliance=context['my_alliance'])[:5]
    except Exception:
        pass

#    TODO: get territories
    context['territories'] = Territory.objects.all()
    return render_to_response('game.html',
                              context,
                              context_instance=RequestContext(request))

