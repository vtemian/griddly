from datetime import datetime
import hashlib
import random
from django.http import HttpResponse
from django.shortcuts import  render, render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from django.utils.hashcompat import sha_constructor

from account.models import PasswordReset
from game import views
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

def base(request):
    if request.user.is_authenticated():
        return views.start(request)
    else:
        return render(request, 'login.html')

def reset_password_instance(request):
    if request.method == 'POST':
        fromEmail = "staff@outclan.com"
        toEmail = request.POST.get('email')
        
        try:
            reset_instance = PasswordReset.objects.get(email=toEmail, done=False)
            return HttpResponse(simplejson.dumps({'message':"There is a request. Please check again!"}))
        except PasswordReset.DoesNotExist:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Outclan - reset password"
            msg['From'] = fromEmail
            msg['To'] = toEmail

            salt = sha_constructor(str(random.random())).hexdigest()[:5]
            token = sha_constructor(salt + toEmail).hexdigest()

            PasswordReset(email=toEmail, token=token).save()

            link = "http://www.outclan.com/password/"+token

            text = "Hi!\n"+link+"\n"
            html = """\
            <html>
              <head></head>
              <body>
                <p>Hi!<br>
                   """+link+"""<br>
                </p>
              </body>
            </html>
            """

            username = 'vtemian'
            password = "seleus00"

            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            msg.attach(part1)
            msg.attach(part2)

            s = smtplib.SMTP('smtp.sendgrid.net', 587)

            s.login(username, password)

            s.sendmail(fromEmail, toEmail, msg.as_string())

            s.quit()
            return HttpResponse(simplejson.dumps({'message':"An email has been sent to you!"}))
    return HttpResponse('Not here!')

def reset_password(request, token):
    reset_instance = PasswordReset.objects.get(token=token)
    now = datetime.datetime.now()
    context = {}
    if now-reset_instance.created_at < datetime.timedelta(minutes=30):
        context['token'] = token
        return render_to_response('change_password.html',
                              context,
                              context_instance=RequestContext(request))
    else:
        reset_instance.done = True
        reset_instance.save()
        context['email'] = reset_instance.email
        return render_to_response('fail_change_password.html',
                              context,
                              context_instance=RequestContext(request))