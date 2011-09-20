from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from territory.models import *
from location.models import *

@csrf_exempt
def create_territory(request):
    if request.method == 'POST':

        up = UserProfile.objects.get(user=request.user)
            
        try:
            terrytories = Territory.objects.get(owner=up)
            return HttpResponse(simplejson.dumps({'error': 'territory'}))
        except Exception:
            area = int(float(request.POST.get('area')))/1000
            money = up.money
            if area/1000 <= money:
                territory = Territory.objects.create(price=0, area=0, owner=up)
                path =  request.POST.get('path')
                print path
                points = path.split(';')
                for point in points:
                    lat = point.split(',')[0]
                    lng = point.split(',')[1]
                    geoPoint = Points.objects.create(lat=lat, lng=lng)
                    territory.points.add(geoPoint)
                up.money = money - area/1000
                loc =  request.POST.get('locations')
                points = loc.split(';')

                for point in points:
                    try:
                        lat = point.split(',')[0]
                        lng = point.split(',')[1]

                        location = Location.objects.get(lat=float(lat), lng=float(lng))
                        location.territory = territory
                        location.save()
                        
                    except Exception:
                        pass
                up.save()
                return HttpResponse(simplejson.dumps({'nice': 'nice'}))
            else:
               return HttpResponse(simplejson.dumps({'error': 'money'}))
    return HttpResponse('Not here!')

@csrf_exempt
def verify_territory(request):
    if request.method == 'POST':
        path =  request.POST.get('path')
        points = path.split(';')
        minx = 999.00
        maxx = -999.00
        miny = 999.00
        maxy = -999.00

        for point in points:
            lat = float(point.split(',')[0])
            lng = float(point.split(',')[1])
            if lat < minx:
                minx = lat
            if lat > maxx:
                maxx = lat
            if lng < miny:
                miny = lng
            if lng >maxy:
                maxy = lng

        locations = Location.objects.filter(lat__range=(minx, maxx), lng__range=(miny, maxy))

        if locations:
            json_locations = []
            for location in locations:
                json_locations.append(simplejson.dumps({'lat': location.lat, 'lng': location.lng}))

            return HttpResponse(simplejson.dumps({'locations': json_locations}))
        else:
            return HttpResponse(simplejson.dumps({'error': minx}))
        
    return HttpResponse('Not here!')