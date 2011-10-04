import hashlib
from django.contrib.auth.models import check_password, User
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import loader
from django.template.context import RequestContext, Context
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from account.models import UserProfile
from checkin.models import Checkin
from notification.models import Notification
from notification.views import accept_friend, un_friend as unfriend
from profile.forms import UserChangePassword, UserChangeEmail, UserChangeFirstName, UserChangeLastName, UserChangePersonalInfo
from profile.models import Friend
from django.db.models import Q
from alliance.models import *

def user_menu(request):
    render_context = {}
    user = UserProfile.objects.get(user=request.user)
    notification = Notification.objects.filter(recipient = user).order_by('created_at')
    unseen_notification = notification.filter(seen=False)
    friend, created = Friend.objects.get_or_create(user=request.user)

    render_context['friend_notification_unseen'] = unseen_notification.filter(Q(type="Friend Request")|Q(type="Unfriend"))
    render_context['message_notification_unseen'] = unseen_notification.filter(type="Message")
    render_context['clan_notification_unseen'] = unseen_notification.filter(type="Clan")
    render_context['notifications'] = unseen_notification
    render_context['userprofile'] = user
    render_context['friends'] = friend.friends
    render_context['friend_notification'] = notification.filter(Q(type="Friend Request")|Q(type="Unfriend"))
    render_context['message_notification'] = notification.filter(type="Message")
    render_context['clan_notification'] = notification.filter(type="Clan")
    render_context['checkins'] = Checkin.objects.filter(user=user)
    render_context['location_checkin'] = render_context['checkins'].values('location').annotate(count=Count('location'))
    print render_context['location_checkin']

    try:
        alliance = Alliance.objects.get(members=user)
        render_context['my_alliance'] = alliance
        if render_context['userprofile'].clan_stream == 'news':
            render_context['clan_stream'] = AllianceNews.objects.filter(alliance=render_context['my_alliance'], type="simple")
    except Exception:
        pass

    return render_context

def myprofile(request):
    user = UserProfile.objects.get(user=request.user)
    return render_to_response('my_profile.html',
                              user_menu(request),
                              context_instance=RequestContext(request))

def profiles(request, profile_id):
    try:
        user = UserProfile.objects.get(pk=profile_id)
        friend, created = Friend.objects.get_or_create(user=user.user)
        context = user_menu(request)
        
        try:
            alliance = Alliance.objects.get(members=user)
            context['alliance'] = alliance
        except Exception:
            pass
        context['userprofileid'] = user
        context['friends'] = friend.friends
        context['friend_request'] = Notification.objects.filter(Q(sender=context['userprofile'], recipient=user) | Q(sender=user, recipient=context['userprofile']), finished=False, type="Friend Request")

        return render_to_response('profile.html',
                                   context,
                                    context_instance=RequestContext(request))
    except Exception:
        redirect('/ranks')

def get_users(request):
    if request.method == 'GET':
        username = request.GET.get('user')
        users = User.objects.filter(username__contains=username)
        results = [ (user.__unicode__()) for user in users ]
        return HttpResponse(simplejson.dumps(results))
    return HttpResponse('Not here!')

@csrf_exempt
def check_user(request):
    if request.method == 'POST':
        if User.objects.filter(username=request.POST.get('user')).exists():
            return HttpResponse('exists')
        else:
            return HttpResponse('not-exists')
    return HttpResponse('Not here!')

@csrf_exempt
def dismiss_clan(request):
    if request.method == 'POST':
        user = UserProfile.objects.get(user=request.user)
        alliance = Alliance.objects.get(members=user)
        alliance_membership = user.alliancemembership_set.filter(alliance=alliance)
        alliance_membership.delete()
        members = alliance.members.all()
        if not members:
            alliance.delete()
        return HttpResponse('nice')
    return HttpResponse('Not here!')

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        up = UserProfile.objects.get(user__username=user)
        notification = Notification.objects.create(message=request.POST.get('message'), sender=UserProfile.objects.get(user=request.user),recipient=up, type="Message")
        notification_template = loader.get_template('notification.html')
        c = Context({ 'notification': notification })
        message = notification_template.render(c)
        return HttpResponse(simplejson.dumps({'user': request.user.username, 'recipient': user, 'message': message, 'type':'message'}))
    return HttpResponse('Not here!')

@csrf_exempt
def widget_lvl(request):
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        profile.widget_left = request.POST.get('left')
        profile.widget_top = request.POST.get('top')
        profile.save()
        return HttpResponse('ok')
    return HttpResponse('Not here!')

@csrf_exempt
def widget_territory(request):
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        profile.territory_widget_left = request.POST.get('left')
        profile.territory_widget_top = request.POST.get('top')
        profile.save()
        return HttpResponse('ok')
    return HttpResponse('Not here!')

@csrf_exempt
def stream_clan(request):
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        profile.clan_stream = 'news'
        profile.save()
        return HttpResponse('ok')
    return HttpResponse('Not here!')

@csrf_exempt
def add_friend_request(request, profile_id):
    if request.method == 'POST':
        user = UserProfile.objects.get(user=request.user)
        exists = UserProfile.objects.filter(pk=profile_id).exists()
        if exists:
            recipient = UserProfile.objects.get(pk=profile_id)
            notification = Notification.objects.create(message="wants to be your friend", sender=user,recipient=recipient, type="Friend Request")
            notification_template = loader.get_template('notification.html')
            c = Context({ 'notification': notification })
            message = notification_template.render(c)
            return HttpResponse(simplejson.dumps({'user': request.user.username, 'recipient': recipient.user.username, 'message': message, 'type':'friend'}))
    else:
        redirect('/profile/' + profile_id)
@csrf_exempt
def un_friend(request, profile_id):
    if request.method == 'POST':
        user = UserProfile.objects.get(user=request.user)
        exists = UserProfile.objects.filter(pk=profile_id).exists()
        if exists:
            recipient = UserProfile.objects.get(pk=profile_id)
            unfriend(recipient=recipient, sender=user)
            Notification(message=" unfriend you", sender=user,recipient=recipient, type="Unfriend", finished=True).save()
            return HttpResponse(simplejson.dumps({'message': 'The request has been submited'}))
    else:
        redirect('/profile/' + profile_id)

@csrf_exempt
def friendrequest(request):
    if request.method == 'POST':
        user = UserProfile.objects.get(user=request.user)
        notification = Notification.objects.get(pk=request.POST.get('id'))
        if request.POST.get('type') == 'accept':
            accept_friend(sender=notification.sender, recipient=user)
        notification.seen=True
        notification.finished=True
        notification.save()
        return HttpResponse(simplejson.dumps({'message': 'You just accepted the friendship'}))
    else:
        redirect('/profile/' + profile_id)

def password_change(request):
    if request.method == 'POST':
        form = UserChangePassword(request.POST)
        if form.is_valid():
            if check_password(request.POST.get('old_password'), request.user.password):
                user = request.user
                user.set_password(request.POST.get('new_password'))
                user.save()
                return HttpResponse(simplejson.dumps({'message': 'The password has been changed'}))
            else:
                 return HttpResponse(simplejson.dumps({'lol': 'Incorect password'}))
        else:
            return HttpResponse(simplejson.dumps(form.errors))
    return redirect('/profile')

def email_change(request):
    if request.method == 'POST':
        form = UserChangeEmail(request.POST)
        if form.is_valid():
            new_email = request.POST.get('email')
            user = request.user
            user.email = new_email
            user.save()
            gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(new_email).hexdigest()
            up = UserProfile.objects.get(user=request.user)
            up.gravatar_url = gravatar_url
            up.save()
            return HttpResponse(simplejson.dumps({'message': 'The email has been changed'}))
        else:
            return HttpResponse(simplejson.dumps(form.errors))
    return redirect('/profile')

def first_name_change(request):
    if request.method == 'POST':
        form = UserChangeFirstName(request.POST)
        if form.is_valid():
            name = request.POST.get('first_name')
            user = request.user
            user.first_name = name
            user.save()
            return HttpResponse(simplejson.dumps({'message': 'The first name has been changed'}))
        else:
            return HttpResponse(simplejson.dumps(form.errors))
    return redirect('/profile')

def last_name_change(request):
    if request.method == 'POST':
        form = UserChangeLastName(request.POST)
        if form.is_valid():
            name = request.POST.get('last_name')
            user = request.user
            user.last_name = name
            user.save()
            return HttpResponse(simplejson.dumps({'message': 'The last name has been changed'}))
        else:
            return HttpResponse(simplejson.dumps(form.errors))
    return redirect('/profile')

def personal_info_change(request):
    if request.method == 'POST':
        form = UserChangePersonalInfo(request.POST)
        if form.is_valid():
            type = request.POST.get('type')
            info = request.POST.get('info')
            user = UserProfile.objects.get(user=request.user)
            if type == 'facebook':
                user.facebook = info
            if type == 'google':
                user.google = info
            if type == 'yahoo':
                user.yahoo = info
            user.save()
            return HttpResponse(simplejson.dumps({'message': 'Changes have been done'}))
        else:
            return HttpResponse(simplejson.dumps(form.errors))
    return redirect('/profile')