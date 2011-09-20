from django.shortcuts import render_to_response, redirect, render
from django.template.context import RequestContext
from account.models import UserProfile
from profile.views import user_menu
from alliance.models import *
from territory.models import *
from battle.models import * 
from django.db.models import Q

def start(request):
    context = user_menu(request)

    try:
        if context['userprofile'].clan_stream == 'news':
            context['news'] = AllianceNews.objects.filter(alliance=context['my_alliance'])[:5]
    except Exception:
        pass

#    TODO: get territories
    territories = Territory.objects.all()

    
    try:
        territories = territories.exclude(owner = context['userprofile'])
    except Exception:
        pass

    context['territories'] = territories

#    context['war'] = Battle.objects.get(Q(attacker=context['userprofile']) | Q(defender=context['userprofile']))
#    context['my_territory'] = Territory.objects.get(owner = context['userprofile'])

    try:
        context['my_territory'] = Territory.objects.get(owner = context['userprofile'])
    except Exception:
        pass
    try:
        context['war'] = Battle.objects.get(Q(attacker=context['userprofile']) | Q(defender=context['userprofile']), active=True)
    except Exception:
        pass

    return render_to_response('game.html',
                              context,
                              context_instance=RequestContext(request))

