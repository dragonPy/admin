from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

SPAN_CHOICES = (
    (0, 'Daily'),
    (1, 'Monthly'),
    (2, 'Yearly'),
)

# all banks users can withdraw from
class Bank(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name=_("Code"))
    name_str_cn = models.CharField(max_length=200, verbose_name=_("Bank Chinese name"))
    card_length_enterprise = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("Enterprise card length"))
    card_length_private = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("Private card length"))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")

# country data
class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    name_en = models.CharField(max_length=100, verbose_name=_("English name"))
    iso2 = models.CharField(max_length=4, unique=True, verbose_name=_("ISO2"))
    mobile_code = models.CharField(max_length=5, verbose_name=_("Mobile code"))

    def __str__(self):
        return self.name_en.encode('ascii','ignore').decode('ascii')

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countrys")

# province & district data
class ProvinceCN(models.Model):  
    district_id = models.CharField(max_length=20, verbose_name=_("District ID"))
    district_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("District name"))
    city_id = models.CharField(max_length=20, verbose_name=_("City ID"))
    city_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("City name"))
    province_id = models.CharField(max_length=20, verbose_name=_("Province ID"))
    province_name = models.CharField(max_length=100, verbose_name=_("Province name"))

    def __str__(self):
        if self.district_id == self.city_id == '0':
            return self.province_name.encode('utf8','ignore')

        if self.district_id == '0':
            return self.province_name.encode('utf8','ignore') + self.city_name.encode('utf8','ignore')

    class Meta:
        verbose_name = _("Chinese Province")
        verbose_name_plural = _("Chinese Provinces")

class Language(models.Model):
    alpha2 = models.CharField(max_length=3, verbose_name=_("alpha2"))
    alpha3b = models.CharField(max_length=4, verbose_name=_("alpha3"))
    english = models.CharField(max_length=100, verbose_name=_("English"))

    def __str__(self):
        return self.english.encode('ascii','ignore').decode('ascii')

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

# Fund Limit Settings
class FundLimit(models.Model):
    span = models.PositiveSmallIntegerField(default=0, choices=SPAN_CHOICES, verbose_name=_("Span"))
    currency = models.CharField(max_length=10, verbose_name=_("Currency"))
    withdraw = models.DecimalField(max_digits=16, decimal_places=8, default=0, blank=True, null=True, verbose_name=_("Withdraw"))
    deposit = models.DecimalField(max_digits=16, decimal_places=8, default=0, blank=True, null=True, verbose_name=_("Deposit"))
    memo = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Memo"))

    def __str__(self):
        return "%s|%s|%s" % (self.memo.encode('ascii', 'ignore').decode('ascii'), self.currency, SPAN_CHOICES[self.span][1])

    class Meta:
        verbose_name = _("Fund Limit")
        verbose_name_plural = _("Fund Limits")

# KYC Condition Settings
class KYCLevel(models.Model):
    alien = models.BooleanField(default=False, verbose_name=_("Alien"))
    level = models.PositiveSmallIntegerField(default=0, verbose_name=_("Level"))
    condition = models.CharField(max_length=200, verbose_name=_("Condition"))
    limits = models.ManyToManyField(FundLimit, blank=True, verbose_name=_("Limits"))

    class Meta:
        verbose_name = _("KYC Level")
        verbose_name_plural = _("KYC Levels")

# Point Level
class PointLevel(models.Model):
    level = models.PositiveSmallIntegerField(default=0, verbose_name=_("Level"))
    level_str = models.CharField(max_length=100, verbose_name=_("Level String"))
    point_upper = models.IntegerField(null=True,blank=True, verbose_name=_("Point upper"))
    point_lower = models.IntegerField(verbose_name=_("Point lower"))
    withdraw_rate = models.FloatField(verbose_name=_("Withdraw rate"))
    loan_leverage = models.FloatField(verbose_name=_("Loan leverage"))

    class Meta:
        verbose_name = _("Point Level")
        verbose_name_plural = _("Point Levels")