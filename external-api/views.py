from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from account.models import UserProfile
from alliance.models import Alliance
from battle.models import Battle
from checkin.models import Checkin
from location.models import Location, Loyalty
from datetime import datetime, timedelta
from nodejs_server.utils import encode_for_socketio
from profile.models import Friend
from territory.models import Territory

def login(request):
    username = request.GET['username']
    password =  request.GET['password']

    user = authenticate(username = username, password = password)
    if user:
        return HttpResponse('login')
    else:
        return HttpResponse('not_logged')

def getbattleresults(battle):
    attackers_checkins = Checkin.objects.filter(user=battle.attacker, battle=battle).count()
    defender_checkins = Checkin.objects.filter(user=battle.defender, battle=battle).count()

    return attackers_checkins - defender_checkins

def checkin_notification(msg):
    pass

def check_loyalty(userProfile):
    loyalties = Loyalty.objects.filter(active=True, userProfile=userProfile)
    for loyalty in loyalties:
        if loyalty.value < 50:
            return False
    return True

def checkingin(request):
    if request.method == 'GET':
        userName = request.GET['username']
        locName = request.GET['checkin']
        locLong = request.GET['lng']
        locLang = request.GET['lat']
        up = UserProfile.objects.get(user__username=userName)
        location, created = Location.objects.get_or_create(name=locName, lng=float(locLong), lat=float(locLang))
        try:
            users = Friend.objects.get(user=up.user).friends.all()
            friends = []
            for user in users:
                if user.friends_stream:
                    friends.append(user)
        except Exception:
            friends = []

        if created:
            location.subscription = 1
            location.save()

        checkin = Checkin(user=up, location=location)
        nowdatetime = datetime.now()

        try:
            battle = Battle.objects.get(Q(attacker=up)|Q(defender=up), active=True)
            try:
                latest_checkin = Checkin.objects.filter(user=up, location=location).order_by('-created_at')[0]
                if (nowdatetime - latest_checkin.created_at) < timedelta (seconds = 1):
                    return HttpResponse('to short')
            except Exception:
                pass

            checkin.created_at = nowdatetime
            checkin.battle = battle
            checkin.save()
            
            my_loyalty, created = Loyalty.objects.get_or_create(location=location, userProfile=up)
            my_loyalty.value += 10

            if battle.attacker == up:
                enemy = battle.defender
            else:
                enemy = battle.attacker



            enemy_loyalty, created = Loyalty.objects.get_or_create(location=location, userProfile=enemy)

            print enemy.user.username

            if check_loyalty(up):
                battle.active = False
                battle.winner = up

                print location.territory
                location.territory.owner = up

                location.territory.save()
                my_loyalty.active = False
                enemy_loyalty.active = False
                battle.save()
            else:

                enemy_loyalty.value -= 10

            enemy_loyalty.save()
            my_loyalty.save()
                
        except Battle.DoesNotExist:
            try:
                latest_checkin = Checkin.objects.filter(user=up, location=location).order_by('-created_at')[0]
                if (nowdatetime - latest_checkin.created_at) < timedelta (seconds = 2):
                    return HttpResponse('to short2')
            except Exception:
                pass

            checkin.created_at = nowdatetime
            checkin.save()

            money_rate = up.lvl * up.lvl
            exp_rate = up.lvl

            if up.lvl == 1:
                money_rate = 5
                exp_rate = 2

            money = float(location.subscription) * money_rate
            exp = location.subscription * exp_rate
            
            up.money += ( money * (100 - up.money_to_all) ) / 100
            up.exp += ( exp * (100 - up.exp_to_all ) ) / 100
            if up.exp >= 5 * up.lvl * up.lvl:
                up.lvl += 1
            up.save()
            
            try:
                alliance = Alliance.objects.get(members=up)
                users = alliance.members.all()
                node_users = []
                for user in users:
                    node_users.append(user.user.username)
                    user.money += up.money_to_all
                    user.exp += up.exp_to_all
                    if user.exp >= 5 * user.lvl * user.lvl:
                        user.lvl += 1
                    user.save()
            except Alliance.DoesNotExist:
                pass
            
            try:
                if location.territory:
                    owner = location.territory.owner
                    if owner:
                        if owner != up:
                            try:
                                owner.exp += up.lvl * location.subscription / Alliance.objects.get(members=up).members.all().count() / 2
                                owner.lvl += up.lvl * up.lvl * location.subscription / 2
                                if owner.exp >= 5 * owner.lvl * owner.lvl:
                                    owner.lvl += 1
                                owner.save()
                            except Alliance.DoesNotExist:
                                pass
            except UserProfile.DoesNotExist:
                pass
            
        if friends:
            return render_to_response('checkin-done.html',
                                  {'friends': friends, 'location':location, 'user':up},
                                  context_instance=RequestContext(request))
        else:
            return HttpResponse('done')

    return HttpResponse('a')
