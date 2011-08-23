from django.shortcuts import  render
from game import views

def base(request):
    if request.user.is_authenticated():
        return views.start(request)
    else:
        return render(request, 'index.html')