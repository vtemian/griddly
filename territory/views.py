from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from territory.models import *

@csrf_exempt
def create_territory(request):
    if request.method == 'POST':
        up = UserProfile.objects.get(user=request.user)
        try:
            terrytories = Territory.objects.get(owner=up)
            print terrytories
            return HttpResponse(simplejson.dumps({'error': 'territory'}))
        except Exception:
            area = int(float(request.POST.get('area')))/10
            money = up.money
            if area/10 <= money:
                territory = Territory.objects.create(price=0, area=0, owner=up)
                path =  request.POST.get('path')
                points = path.split(';')
                for point in points:
                    lat = point.split(',')[0]
                    lng = point.split(',')[1]
                    geoPoint = Points.objects.create(lat=lat, lng=lng)
                    territory.points.add(geoPoint)
                up.money = money - area/10
                up.save()
                return HttpResponse(simplejson.dumps({'nice': 'nice'}))
            else:
               return HttpResponse(simplejson.dumps({'error': 'money'}))
    return HttpResponse('Not here!')