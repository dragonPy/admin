from __future__ import unicode_literals

from django.db import models

class KYCRequestDomesticPhotoHold(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name_str_cn = models.CharField(max_length=200)
    card_length_enterprise = models.CharField(max_length=200, null=True, blank=True)
    card_length_private = models.CharField(max_length=200, null=True, blank=True)