#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import redis
import base64
import datetime
import smtplib
from string import ascii_lowercase, digits
from email.mime.text import MIMEText
from email.header import Header
from random import randint, choice
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

VERIFICATION_SENT = _('Verification Sent')
INVALID_INTERVAL = _('Invalid Interval')
SALT = ''
INTERVAL = 30

r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Mail Conf
sender = 'noreply@cyanide.io'
username = sender
smtpserver = 'smtp.zoho.com'
password = 'C2y1a3n4i5de'

CONTENT = """
    <html>
    <p> 
        Hello, your verification code is: <b>%s</b>
    </p> 
    <b>
        Cyanide.io
    </b>
    </html>
"""

def get_username_from_email(email):
    try:
        return User.objects.get(email=email).username
    except Exception:
        return None

def generate_random_username(length=10, chars=ascii_lowercase+digits, split=4, delimiter='-'):
    
    username = ''.join([choice(chars) for i in xrange(length)])
    
    if split:
        username = delimiter.join([username[start:start+split] for start in range(0, len(username), split)])
    
    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username;

def send_mail(vcode, receiver):
    TITLE = "Mail From Cyanide.io"
    try:
        msg = MIMEText(CONTENT % vcode,'html','utf-8')
        if not isinstance(TITLE, unicode):
            TITLE = unicode(TITLE, 'utf-8')
        msg['Subject'] = TITLE
        msg['From'] = sender
        msg['To'] = receiver
        msg["Accept-Language"]="en-US"
        msg["Accept-Charset"]="ISO-8859-1, utf-8"
        smtp = smtplib.SMTP_SSL(smtpserver, 465)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        return True
    except Exception, e:
        print str(e)
        return False

def get_real_username(email):
    return base64.b64encode("".join([str(c)+SALT for c in email]))

# def get_email(real_username):
#     return "".join(base64.b64decode(real_username).split(SALT))

def gen_verification_code(num):
    vcode = str(randint(1000, 9999))
    if send_mail(vcode, num):
        return vcode
    else:
        return False

def got_vcode(vcode_key, vcode, vcode_ts_key):
    if vcode:
        r.set(vcode_key, vcode)
        r.set(vcode_ts_key, datetime.datetime.now().strftime("%s")) 
        return unicode(VERIFICATION_SENT), 1, vcode
    else:
        return unicode(INVALID_INTERVAL), 0, 0

def send_vcode(real_username, email):
    vcode_key = real_username
    vcode_ts_key = "%s_ts" % real_username
    ts = r.get(vcode_ts_key)
    if ts == None:
        vcode = gen_verification_code(email)
        return got_vcode(vcode_key, vcode, vcode_ts_key)
    else:
        if (int(datetime.datetime.now().strftime("%s")) - int(ts)) >= INTERVAL:
            vcode = gen_verification_code(email)
            return got_vcode(vcode_key, vcode, vcode_ts_key)
        else:
            return unicode(INVALID_INTERVAL), 0, 0

def vcode_verified(email, vcode):
    verified = vcode == r.get(get_real_username(email))
    if verified:
        # When verified, delete keys
        r.delete(get_real_username(email))
        r.delete("%s_ts" % get_real_username(email))
    return verified
