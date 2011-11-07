import os
from django.http import HttpResponse
from django.utils import simplejson
from alliance.forms import ClanCreate, UploadAvatar, NewsCreate, ClanChangeName
from alliance.models import Alliance, AllianceMembership, AllianceNews, Like, Unlike
from django.views.decorators.csrf import csrf_exempt
from profile.models import UserProfile
from notification.models import Notification
from django.template import loader
from django.template.context import RequestContext, Context
from django.shortcuts import render_to_response, redirect, render
from profile.views import user_menu
from common.utils.json_encoder import LazyEncoder


def my_clan(request):
    context = user_menu(request)
    
    my_clan = context['my_alliance']

    context['clan_members'] = AllianceMembership.objects.filter(alliance=my_clan)
    context['avatar_form'] = UploadAvatar()
    context['clan_stream'] = AllianceNews.objects.filter(alliance=Alliance.objects.get(members=context['userprofile']))
    context['boss'] = context['clan_members'].get(rank=1).profile
    context['rank'] = context['userprofile'].alliancemembership_set.all()[0].rank
    
    last_lvl_exp = (my_clan.lvl-1)*(my_clan.lvl-1)*10
    exp_needed = ((my_clan.lvl*my_clan.lvl)*10)- last_lvl_exp

    context['exp'] = ((my_clan.exp-last_lvl_exp)*100)/exp_needed
    
    return render_to_response('my_clan2.html',
                              context,
                              context_instance=RequestContext(request))

def create(request):
    if request.method == 'POST':
        form = ClanCreate(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            clan = Alliance.objects.create(name=name)
            user = UserProfile.objects.get(user=request.user)
            AllianceMembership(alliance=clan, profile=user, rank='1').save()
            user.save()
            return HttpResponse(simplejson.dumps({'message': 'Clan registered'}))
        else:
            return HttpResponse(simplejson.dumps(form.errors))
    else:
        return HttpResponse('ok')
    
@csrf_exempt
def request(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        up = UserProfile.objects.get(user__username=user)

        try:
            notification = Notification.objects.get(message=" invites you in " + request.POST.get('name'), sender=UserProfile.objects.get(user=request.user), recipient=up, type="Clan", finished=False)

            return HttpResponse(simplejson.dumps({'finished': "not"}))
        except Exception:
            notification = Notification.objects.create(message=" invites you in " + request.POST.get('name'), sender=UserProfile.objects.get(user=request.user), recipient=up, type="Clan")
            notification_template = loader.get_template('notification.html')
            c = Context({'notification': notification })
            message = notification_template.render(c)
            return HttpResponse(simplejson.dumps({'user': request.user.username, 'recipient': user, 'message': message, 'type':'clan'}))
      
    return HttpResponse('Not here!')

@csrf_exempt
def process_request(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        notification = Notification.objects.get(pk=request.POST.get('id'))
        if not notification.finished:
            notification.finished = True
            notification.save()
            if type == 'accept':
                clan = Alliance.objects.get(members=notification.sender)
                up = UserProfile.objects.get(user=request.user)
                try:
                    membership = AllianceMembership.objects.get(profile=up, alliance=clan)
                    return HttpResponse(simplejson.dumps({"error": "You are in this clan!"}))
                except Exception:
                    try:
                        membership = AllianceMembership.objects.get(profile=up)
                        membership.delete()
                    except Exception:
                        AllianceMembership(alliance=clan, profile=up, rank="2").save()
                        return HttpResponse(simplejson.dumps({"message": "Clan request accepted!"}))
        else:
            return HttpResponse(simplejson.dumps({"error": "This request is finished"}))
    return HttpResponse('Not here!')

@csrf_exempt
def get_stream(request):
    if request.method == 'GET':
        profile = UserProfile.objects.get(user=request.user)
        news = AllianceNews.objects.filter(alliance=Alliance.objects.get(members=profile))[:5]
        return render_to_response('clan_stream.html',
                              {'clan_stream': news},
                              context_instance=RequestContext(request))
    return HttpResponse('Not here!')

@csrf_exempt
def upload_avatar(request):
    if request.method == 'POST':
        alliance = Alliance.objects.get(members=UserProfile.objects.get(user=request.user))
        form = UploadAvatar(request.POST, request.FILES, instance=alliance)
        if form.is_valid():
            form.save()
            img_path = '<img src="'+alliance.avatar.url+'" alt="image" width="140px" height="140px"/>'
            return HttpResponse(simplejson.dumps({'img': img_path}))
        else:
            print form.errors
            return HttpResponse(simplejson.dumps(form.errors))
    return HttpResponse('Not here!')

def save_file(filename, data):
        file = open(os.path.join('/home/static/', filename), 'w')
        file.write(data)
        file.close()
        return filename

@csrf_exempt
def create_news(request):
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        alliance = Alliance.objects.get(members=profile)
        news = AllianceNews.objects.create(profile=profile, alliance=alliance)
        form = NewsCreate(request.POST, instance=news)
        if form.is_valid:
            form.save()
            
            users = alliance.members.all().filter(clan_stream='news').exclude(user=profile.user)
            json_users = []
            for user in users:
                json_users.append(user.user.username)

            stream_template = loader.get_template('news.html')
            c = Context({'news': news })
            message = stream_template.render(c)

            return HttpResponse(simplejson.dumps({'message':'gg', 'users':json_users, 'news':message}))
        else:
            return HttpResponse(simplejson.dumps(form.errors))
    return redirect('/clan')

@csrf_exempt
def vote_news(request):
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        type = request.POST.get('type')
        news = AllianceNews.objects.get(pk=request.POST.get('id'))

        if type == 'like':
            try:
                unlike = AllianceNews.objects.get(unlike__profile=profile, pk=request.POST.get('id')).unlike.filter(profile=profile)
                unlike.delete()
            except Exception:
                pass
            vote = Like.objects.create(profile=profile)
            news.like.add(vote)
        else:
            try:
                like = AllianceNews.objects.get(like__profile=profile, pk=request.POST.get('id')).like.filter(profile=profile)
                like.delete()
            except Exception:
                pass
            vote = Unlike.objects.create(profile=profile)
            news.unlike.add(vote)

        news.save()

        return HttpResponse('ok')
    return HttpResponse('Sorry dude, not here!')

@csrf_exempt
def check_like_state(request):
    if request.method == 'GET':
        profile = UserProfile.objects.get(user=request.user)

        try:
            AllianceNews.objects.get(pk=request.GET.get('id'), like__profile=profile)
            return HttpResponse('is-like')
        except Exception:
            if AllianceNews.objects.filter(pk=request.GET.get('id'), unlike__profile=profile).exists():
                return HttpResponse('is-unlike')
            else:
                return HttpResponse('ok')
    return HttpResponse('Sorry dude, not here')

@csrf_exempt
def del_member(request):
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        print request.POST.get('username')
        try:
            deleted_member = UserProfile.objects.get(user__username=request.POST.get('username'))
            clan = Alliance.objects.get(members=profile)
            AllianceMembership.objects.get(alliance=clan, profile=deleted_member).delete()
            return HttpResponse(simplejson.dumps({'message': "The user have been succesfuly removed from your clan!"}))
        
        except AllianceMembership.DoesNotExist:
            return HttpResponse(simplejson.dumps({'error': 'The user is not in this clan any more!'}))
        except UserProfile.DoesNotExist:
            return HttpResponse(simplejson.dumps({'error': "The user doesn't exists anymore!"}))
        
    return HttpResponse('Not here!')

def name_change(request):
    if request.method == 'POST':
        alliance = Alliance.objects.get(members=UserProfile.objects.get(user=request.user))
        form = ClanChangeName(request.POST, instance=alliance)
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({'message': 'The name has been changed!'}))
        else:
            return HttpResponse(simplejson.dumps(form.errors))
    return HttpResponse('Not here!')