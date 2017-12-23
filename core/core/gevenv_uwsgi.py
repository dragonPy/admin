import os, django
from gevent import monkey
from django.core.handlers.wsgi import WSGIHandler as DjangoWSGIApp

monkey.patch_all()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
application = DjangoWSGIApp()
