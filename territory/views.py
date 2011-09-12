from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from territory.models import *

@csrf_exempt
def create_territory(request):
    if request.method == 'POST':
        territory = Territory.objects.create(price=0, area=0)
        path =  request.POST.get('path')
        points = path.split(';')
        for point in points:
            lat = point.split(',')[0]
            lng = point.split(',')[1]
            geoPoint = Points.objects.create(lat=lat, lng=lng)
            territory.points.add(geoPoint)
    return HttpResponse('Not here!')