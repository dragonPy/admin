"""core URL Configuration """
import os
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

from django.conf.urls import url, include

# Custom APIS
from users.auth.api import login, register, verify

from tastypie.api import Api
from users.api.resources import *

DEBUG = int(os.environ['DEBUG'])
if not DEBUG:
    IS_ADMIN = int(os.environ['IS_ADMIN'])

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(UserWithdrawStatusResource())
v1_api.register(UserLoginHistoryResource())
v1_api.register(UserBankInfoResource())
v1_api.register(UserAuthorizationResource())
v1_api.register(UserProfileResource())
v1_api.register(UserStatusResource())
v1_api.register(UserAccessKeyResource())
v1_api.register(UserChangePwdAtResource())
v1_api.register(UserConfigResource())
v1_api.register(UserRequestResource())

APIS = [ 
    url(r'^api/', include(v1_api.urls)),
    url(r'^login/', login, name='login'),                                           # Custom.Login API
    url(r'^register/', register, name='register'),                                  # Custom.Register API
    url(r'^verify/', verify, name='verify'),                                        # Custom.Verify API
]

ADMIN_URLS = i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),                                      # Django Admin URLS
    url(r'^queue/', include('django_rq.urls')),                                     # Redis Queue Management
)
if DEBUG:
    urlpatterns = APIS
    urlpatterns += ADMIN_URLS
else:
    urlpatterns = [] if IS_ADMIN else APIS
    if IS_ADMIN:
        urlpatterns += ADMIN_URLS