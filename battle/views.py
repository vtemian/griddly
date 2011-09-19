from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.utils import simplejson
from account.models import UserProfile
from battle.models import Battle
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def war_request(request):
    if request.method == 'POST':
        up = UserProfile.objects.get(user=request.user)
        try:
            battle = Battle.objects.get(Q(attacker=up) | Q(defender=up), active=True)
            return HttpResponse(simplejson.dumps({'error': 'You are in battle'}))
        except Exception:
            defender = UserProfile.objects.get(user__username = request.POST.get('username'))
            Battle(attacker=up, defender=defender).save()
            return HttpResponse(simplejson.dumps({'nice': 'Nice'}))
    else:
        return HttpResponse('Not here')