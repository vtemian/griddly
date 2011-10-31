from django.http import HttpResponse

def blitz(request):
    return HttpResponse('42')