from django.shortcuts import render_to_response
from django.template.context import RequestContext
from account.models import UserProfile
from profile.views import user_menu

def ranks(request):
    users = UserProfile.objects.all().order_by('lvl', 'user__username')
    context = user_menu(request)
    context['users'] = users
    return render_to_response('ranks.html',
                              context,
                              context_instance=RequestContext(request))