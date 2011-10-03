from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext, Context
from battle.models import Battle
from checkin.models import Checkin
from territory.forms import ChangeName, ChangeColor
from territory.models import *
from location.models import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_territory(request):
    if request.method == 'POST':

        up = UserProfile.objects.get(user=request.user)
            
        try:
            terrytories = Territory.objects.get(owner=up)
            return HttpResponse(simplejson.dumps({'error': 'You stupid asshole, just a territory! Go and conquer something!!!'}))
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
                return HttpResponse(simplejson.dumps({'nice': 'Congratz! You have a territory :)', 'id': territory.id}))
            else:
               return HttpResponse(simplejson.dumps({'error': "Sry...you don't have enough money"}))
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
            return HttpResponse(simplejson.dumps({'error': "There aren't any locations in this territory!"}))

        
    return HttpResponse('Not here!')

def load_territory(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        territory = Territory.objects.get(pk=id)
        checkins = Checkin.objects.filter(location__territory = territory).order_by('-created_at')[:5]
        locations = Location.objects.filter(territory=territory)
        notification_template = loader.get_template('territory_widget.html')
        context = {}
        context['territory'] = territory
        context['checkins'] = checkins
        context['locations'] = locations

        try:
            battle = Battle.objects.get(defender = territory.owner, active=True)
            context['battle'] = battle
        except Exception:
            pass
        
        c = Context(context)
        message = notification_template.render(c)
        return HttpResponse(message)
    return HttpResponse('Not good enough')

@csrf_exempt
def upgrade(request):
    if request.method == 'POST':
        id = request.POST.get('id')

        territory = Territory.objects.get(pk=id)
        up = UserProfile.objects.get(user=request.user)

        if up.money >= territory.lvl * 1000:
            territory.lvl = territory.lvl + 1
            territory.save()
            up.money = up.money - territory.lvl * 1000
            up.save()
            return HttpResponse(simplejson.dumps({'message': "You've just upgrade your territory"}))
        return HttpResponse(simplejson.dumps({'message': 'You need ' +str(territory.lvl * 1000) + ' outcoins to upgrade your territory!'}))
    return HttpResponse(simplejson.dumps({'message': "Just a system error! Don't panic...."}))

@csrf_exempt
def change_name(request):
    if request.method == 'POST':
        terid = request.POST.get('id')
        territory = Territory.objects.get(pk=terid)
        form = ChangeName(request.POST, instance=territory)
        form.save()
        return HttpResponse(simplejson.dumps({'message': 'The name has been change!'}))
    return HttpResponse('Not here!')

@csrf_exempt
def change_color(request):
    if request.method == 'POST':
        terid = request.POST.get('id')
        territory = Territory.objects.get(pk=terid)
        form = ChangeColor(request.POST, instance=territory)
        form.save()
        return HttpResponse(simplejson.dumps({'message': 'The color has been change!'}))
    return HttpResponse('Not here!')