from django.shortcuts import render_to_response
from django.template.context import RequestContext
from account.models import UserProfile
from profile.views import user_menu
from django.contrib.auth.decorators import login_required

@login_required(login_url='/user/login/')
def ranks(request):
    users = UserProfile.objects.all().order_by('-lvl', '-money', 'user__username')
    context = user_menu(request)
    context['users'] = users
    return render_to_response('ranks.html',
                              context,
                              context_instance=RequestContext(request))