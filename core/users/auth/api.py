#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import time
import datetime
from django.utils import timezone
from tastypie.models import ApiKey
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.core import serializers
from users.models import VaultUser as UserProfile

from users.auth.utils import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import requests
import random
import django_rq

# for wechat oauth
# WECHAT_URL = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s'

queue = django_rq.get_queue('mail')

VER_PURPOSE_LIST = ['register', 'retrieve']

USER_EXISTS = _('User Exists')
USER_INVALID = _('User Invalid')
INVALID_PURPOSE = _('Purpose Invalid')
INVALID_PARAM = _('Parameter Invalid')
USER_AUTHENTICATED = _('User Authenticated')
USRNAME_PWD_INCORRECT = _('Username or Password Incorrect')
CREDENTIAL_INCORRECT = _('Credential Incorrect')
USER_DISABLED = _('User Disabled')
SUCCEED = _('Succeed')

# Authorization with OAuthToken
def oauth_token_auth(token, username):
    GenderDict = { 1:0, 0:1 }
    try:
        r = requests.get(WECHAT_URL % (token, username))
    except Exception:
        return None, None
    r.encoding = 'utf-8'
    if 'errcode' in r.json().keys():
        return None, None
    else:
        try:
            _user, user_created = User.objects.get_or_create(username=username)
        except Exception:
            print username
            return None
        profile = UserProfile.objects.get(user=_user)
        profile.oauth_token = token
        if user_created:
            profile.nickname = '%s_%s_%s' % (r.json()['nickname'], str(int(time.time())), str(random.randint(1,9)))
            profile.gender = GenderDict[int(r.json()['sex'])]
            profile.avatar = r.json()['headimgurl']
        profile.save()
        return _user, user_created

def user_auth(username, password=None, oauth_token=None, login=False):
    real_username = get_username_from_email(username)
    if not real_username:
        return None, None
    user = None
    new = None
    # 两种密文中同时只能使用一种
    if sum(map(lambda x: 1 if x else 0, [password, oauth_token])) != 1:
        # TODO logging
        return user, None

    if password:
        user = authenticate(username=real_username,password=password)

    elif oauth_token:
        user, new = oauth_token_auth(token=oauth_token, username=username)

    if user is not None and login:
        refresh_apikey(user)
        user._last_login = user.last_login
        user.last_login = timezone.now()
        user.save()

    return user, new

def refresh_apikey(user):
    key = ApiKey.objects.get(user=user)
    key.key = key.generate_key()
    key.save()

# Login API
@csrf_exempt
def login(request):
    # Return Message for login
    R = {
        'is_authenticated': 0,
        'msg': '',
    }
    username = request.POST.get("email", "")
    password = request.POST.get("password", "")
    oauth_token = request.POST.get("oauth_token", "")

    if sum(map(lambda x: 1 if x else 0, [password, oauth_token])) != 1:
        R['is_authenticated'] = 0
        R['msg'] = unicode(CREDENTIAL_INCORRECT)

    user, new = user_auth(username=username, password=password, oauth_token=oauth_token, login=True)
    if user is not None:
        if user.is_active:
            profile = UserProfile.objects.get(user=user)
            key = ApiKey.objects.get(user=user).key
            R['is_authenticated'] = 1
            R['msg'] = unicode(USER_AUTHENTICATED)
            R['key']= key
            R['user_info'] = json.loads(serializers.serialize('json', [user]))[0]['fields']
            R['user_info'].pop('password')
            R['user_info'].pop('is_active')
            R['user_info'].pop('is_superuser')
            R['user_info'].pop('is_staff')
            R['user_info'].pop('user_permissions')
            R['user_info'].pop('groups')
            R['user_profile'] = json.loads(serializers.serialize('json', [profile]))[0]['fields']
            R['profile_id'] = profile.id
            R['user_id'] = user.id
            R['new'] = new
        else:
            R['is_authenticated'] = 0
            R['msg'] = unicode(USER_DISABLED)
    else:
        R['is_authenticated'] = 0
        R['msg'] = unicode(USRNAME_PWD_INCORRECT)

    return JsonResponse(R)

# Register API
@csrf_exempt
def register(request):
    # Return Message for register
    R_REG = {
        'retrieve_succeed': 0,
        'register_succeed': 0,
        'msg': '',
    }

    username = request.POST.get("email", "")
    password = request.POST.get("password", "")
    vcode = request.POST.get("vcode", "")

    if username + password + vcode != "":
        if vcode_verified(username, vcode):
            _username = get_username_from_email(username)
            if not _username:
                _username = generate_random_username()
            _user, user_created = User.objects.get_or_create(username=_username)
            _user.set_password(password)
            if user_created:
                # Set Email Address and Username
                _user.email = username
                R_REG['msg'] = unicode(SUCCEED)
                R_REG['register_succeed'] = 1
                key = ApiKey.objects.get(user=_user).key
                profile = UserProfile.objects.get(user=_user)
                profile.save()
                R_REG['key']= key
                R_REG['user_info'] = json.loads(serializers.serialize('json', [_user]))[0]['fields']
                R_REG['user_profile'] = json.loads(serializers.serialize('json', [profile]))[0]['fields']
                R_REG['user_info'].pop('password')
                R_REG['user_info'].pop('is_active')
                R_REG['user_info'].pop('is_superuser')
                R_REG['user_info'].pop('is_staff')
                R_REG['user_info'].pop('user_permissions')
                R_REG['user_info'].pop('groups')
                R_REG['profile_id'] = profile.id
                R_REG['user_id'] = _user.id
            else:
                R_REG['retrieve_succeed'] = 1
            _user.save()
    else:
        R_REG['msg'] = unicode(INVALID_PARAM)
        R_REG['register_succeed'] = 0
        # Wrong
    return JsonResponse(R_REG)

# Verification Code API
@csrf_exempt
def verify(request):
    # Return Message for register
    UUID_VALID = True
    R_VER = {
        'v_code_sent': 0,
        'msg': '',
    }
    username = request.POST.get("email", "")
    purpose = request.POST.get("purpose", "")  
    real_username = get_real_username(username)

    try:
        validate_email(username)
    except ValidationError as e:
        UUID_VALID = False

    if purpose in VER_PURPOSE_LIST and username != '' and UUID_VALID:
        try:
            _user = User.objects.get(email=username)
            if purpose == 'register':
                R_VER['msg'] = unicode(USER_EXISTS)
                R_VER['v_code_sent'] = 0
            else:
                queue.enqueue(send_vcode, real_username, email=username)
                R_VER['msg'], R_VER['v_code_sent'] = 'VCodeSent', 1
        except ObjectDoesNotExist:
            if purpose == 'retrieve':
                R_VER['msg'] = unicode(USER_INVALID)
                R_VER['v_code_sent'] = 0
            else:
                queue.enqueue(send_vcode, real_username, email=username)
                # q.enqueue_call(func=send_vcode, args=(real_username, username), timeout=30)
                R_VER['msg'], R_VER['v_code_sent'] = 'VCodeSent', 1
    else:
        R_VER['msg'] = unicode(INVALID_PURPOSE)
        R_VER['v_code_sent'] = 0
    return JsonResponse(R_VER)
