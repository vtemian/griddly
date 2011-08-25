from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'common.views.base'),
    url(r'^user/login/', 'account.views.login'),
    url(r'^logout/?$',  'django.contrib.auth.views.logout_then_login'),
    url(r'^user/register/$',  'account.views.register'),
    url(r'^user/change_password/$',  'account.views.password_change'),
    url(r'^profile/$',  'account.views.profile'),
    url(r'^game/?$',  'game.views.start'),
    url(r'^external-api/login/$',  'external-api.views.login'),
    url(r'^external-api/checkin/$',  'external-api.views.checkingin'),
)

urlpatterns += staticfiles_urlpatterns()