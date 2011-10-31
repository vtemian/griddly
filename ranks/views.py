from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import RequestContext, Context
from account.models import UserProfile
from profile.views import user_menu
from django.contrib.auth.decorators import login_required

@login_required(login_url='/user/login/')
def ranks(request):
    users = UserProfile.objects.all().order_by('-lvl', '-money', 'user__username')[:10]
    context = user_menu(request)
    context['users'] = users
    return render_to_response('ranks.html',
                              context,
                              context_instance=RequestContext(request))
@login_required(login_url='/user/login/')
def get_ranks(request, limit):
    users = UserProfile.objects.all().order_by('-lvl', '-money', 'user__username')[int(limit)-10:int(limit)]
    notification_template = loader.get_template('user_ranks.html')
    c = Context({ 'users': users })
    message = notification_template.render(c)
    return HttpResponse(message)
