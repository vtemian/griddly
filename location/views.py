from django.http import HttpResponse
from django.utils import simplejson
from location.models import Location

def get_locations(request):
    locations = Location.objects.all()
    locations_json = []
    for location in locations:
        locations_json.append({'lat': location.lat, 'lng': location.lng, 'name': location.name})
    return HttpResponse(simplejson.dumps({'locations': locations_json}))