from __future__ import unicode_literals
import os, uuid
import requests
import json

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from users.validators import validate_user_config
from core_settings.models import KYCLevel, PointLevel
from django.utils.translation import ugettext_lazy as _

ID_IMG_STATUS = (
    (0, 'null'),
    (1, 'pending'),
    (2, 'invalid'),
    (3, 'verified'),
)

COMPLIANCE_LOCK_STATUS = (
    (0, 'unlocked'),
    (1, 'locked'),
    (2, 'untriggered')
)

GENDER = (
    (0, 'male'),
    (1, 'female')
)

# Timeout is counted in seconds
SERVICE_REQ_TIMEOUT = 3
KYC_SERVICE_HOST = 'http://127.0.0.1:8000'


def genSecret():
    return os.urandom(24).encode('hex')

class BaseModel(models.Model):
    def clean(self, *args, **kwargs):
        # add custom validation here
        super(BaseModel, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class VaultUser(BaseModel):
    user = models.OneToOneField(User, blank=True, null=True, related_name='vault_user')
    # mobile = models.CharField(max_length=11, unique=True, blank=True, null=True, verbose_name=_("Mobile"))
    # Hashed values below
    user_pass_trade = models.CharField(max_length=40, blank=True, verbose_name=_("User trade password"))

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def clean(self, *args, **kwargs):
        super(VaultUser, self).clean(*args, **kwargs)

    # Withdraw rules
    def getWithdrawStatus(self):
        try:
            return UserWithdrawStatus.objects.get(user_id=self.id)
        except UserWithdrawStatus.DoesNotExist:
            raise ValidationError(_('user withdraw status missing'))

    # Authorization Status
    def getAuthorization(self):
        try:
            return UserAuthorization.objects.get(user_id=self.id)
        except UserAuthorization.DoesNotExist:
            raise ValidationError(_('user authorization missing'))

    # Realname, country etc.
    def getProfile(self):
        try:
            return UserProfile.objects.get(user_id=self.id)
        except UserProfile.DoesNotExist:
            raise ValidationError(_('user profile missing'))

    # User Level / KYC etc.
    def getStatus(self):
        try:
            return UserStatus.objects.get(user_id=self.id)
        except UserStatus.DoesNotExist:
            raise ValidationError(_('user profile missing'))

    # Bank Card Info
    def getBankCards(self):
        return UserBankInfo.objects.filter(user_id=self.id)

    # Change Password History
    def getPwdChangeHistory(self):
        return UserChangePwdAt.objects.filter(user_id=self.id)

    # AccessTokens
    def getAccessTokens(self):
        return UserAccessToken.objects.filter(user_id=self.id)

    # Login History
    def getLoginHistory(self):
        return UserLoginHistory.objects.filter(user_id=self.id)

class UserMixin(object):
    """
    # Provides Mutual Methods about a user
    """
    def getUser(self):
        try:
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            raise ValidationError(_('user missing'))

class UserWithdrawStatus(BaseModel, UserMixin):
    """
    # User Signal (signals.py)
    """
    user_id = models.IntegerField(unique=True, verbose_name=_("UserId"))
    daily_btc_withdraw_limit = models.DecimalField(max_digits=16, decimal_places=8, default=0, verbose_name=_("Daily btc withdraw limit"))
    daily_cny_withdraw_limit = models.DecimalField(max_digits=16, decimal_places=8, default=0, verbose_name=_("Daily cny withdraw limit"))
    daily_ltc_withdraw_limit = models.DecimalField(max_digits=16, decimal_places=8, default=0, verbose_name=_("Daily ltc withdraw limit"))
    once_cny_withdraw_limit = models.DecimalField(max_digits=16, decimal_places=8, default=0, verbose_name=_("Once cny withdraw limit"))
    max_cny_withdraw_limit = models.DecimalField(max_digits=16, decimal_places=8, default=0, verbose_name=_("Max cny withdraw limit"))
    withdrawfeeoverride = models.FloatField(blank=True, null=True, verbose_name=_("Withdraw fee override"))

    class Meta:
        verbose_name = _("User withdraw status")
        verbose_name_plural = _("User withdraw statuses")

class UserAuthorization(BaseModel, UserMixin):
    """
    # User Signal (signals.py)
    """
    user_id = models.IntegerField(unique=True, verbose_name=_("UserId"))
    user_login_attempts = models.PositiveSmallIntegerField(default=0, verbose_name=_("User login attempts"))
    otpkey = models.CharField(default=None, max_length=16, null=True, blank=True, verbose_name=_("otpkey"))
    locked = models.DateTimeField(default=None, null=True, blank=True, verbose_name=_("locked"))

    class Meta:
        verbose_name = _('User authorization')
        verbose_name_plural = _('User authorizations')

class UserProfile(BaseModel, UserMixin):
    """
    # User Signal (signals.py)
    """
    user_id = models.IntegerField(unique=True, verbose_name=_("UserId"))
    real_name = models.CharField(max_length=200, default=None, null=True, blank=True, verbose_name=_("Real name"))
    id_number = models.CharField(max_length=50, default=None, null=True, blank=True, verbose_name=_("ID number"))
    id_type = models.IntegerField(default=0, verbose_name=_("ID type"))
    id_type_other = models.CharField(max_length=50, default=None, null=True, blank=True, verbose_name=_("ID type other"))
    gender = models.PositiveSmallIntegerField(default=0, choices=GENDER, verbose_name=_("Gender"))
    birth_date = models.DateField(default=None, null=True, blank=True, verbose_name=_("Birth date"))
    language = models.ForeignKey('core_settings.Language', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name=_("Language"))
    # Start: GeoLocation Info
    country = models.ForeignKey('core_settings.Country', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name=_("Country"))
    state = models.CharField(max_length=64, default=None, null=True, blank=True, verbose_name=_("State"))
    city = models.CharField(max_length=64, default=None, null=True, blank=True, verbose_name=_("City"))
    address = models.CharField(max_length=128, default=None, null=True, blank=True, verbose_name=_("Address"))
    postal_code = models.CharField(max_length=32, default=None, null=True, blank=True, verbose_name=_("Postal code"))
    # End;

    def has_realname(self):
        return self.real_name == ''

    def has_id_number(self):
        return self.id_number == ''

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

class UserStatus(BaseModel, UserMixin):
    """
    # User Signal (signals.py)
    """
    user_id = models.IntegerField(unique=True, verbose_name=_("UserId"))
    phone_verified = models.BooleanField(default=False, verbose_name=_("Phone verified"))
    email_verified = models.BooleanField(default=False, verbose_name=_("Email verified"))
    kyc_verified = models.BooleanField(default=False, verbose_name=_("Kyc verified"))
    id_expire_date = models.DateField(default=None, null=True, blank=True, verbose_name=_("ID expire date"))
    id_expire_date_verified = models.BooleanField(default=False, verbose_name=_("ID expire date verified"))
    id_images_status = models.PositiveSmallIntegerField(default=0, choices=ID_IMG_STATUS, verbose_name=_("ID images status"))
    compliance_lock_status = models.PositiveSmallIntegerField(default=2, choices=COMPLIANCE_LOCK_STATUS, verbose_name=_("Compliance lock status"))
    kyc_level = models.PositiveSmallIntegerField(default=0, verbose_name=_("Kyc level"))
    experience_level = models.PositiveSmallIntegerField(default=0, verbose_name=_("Experience level"))
    point = models.FloatField(default=0, verbose_name=_("Point"))

    def getKYCLevel(self):
        return KYCLevel.objects.get(level=self.kyc_level)

    def getPointLevel(self):
        return PointLevel.objects.get(level=self.experience_level)

    def clean(self, *args, **kwargs):
        pass

    class Meta:
        verbose_name = _('User status')
        verbose_name_plural = _('User statuses')

class UserConfig(models.Model):
    user_id = models.IntegerField(verbose_name=_("UserId"))
    name = models.CharField(max_length=200, validators=[validate_user_config], verbose_name=_("Name"))
    value = models.CharField(max_length=200, verbose_name=_("Value"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    modified = models.DateTimeField(verbose_name=_("Modified"))

    class Meta:
        verbose_name = _('User config')
        verbose_name_plural = _('User config')

class UserBankInfo(BaseModel, UserMixin):
    user_id = models.IntegerField(verbose_name=_("UserId"))
    bank = models.ForeignKey('core_settings.Bank', on_delete=models.DO_NOTHING, verbose_name=_("Bank"))
    cny_bank_account = models.CharField(max_length=255, verbose_name=_("Cny bank account"))
    cny_bank_name = models.CharField(max_length=255, verbose_name=_("Cny bank name"))
    cny_bank_beneficiary = models.CharField(max_length=255, verbose_name=_("Cny bank beneficiary"))

    cny_bank_province = models.ForeignKey('core_settings.ProvinceCN',
        on_delete=models.DO_NOTHING, limit_choices_to={'city_id': 0, 'district_id': 0},
        related_name='cny_bank_province_name', verbose_name=_("Cny bank province"))
    cny_bank_city = models.ForeignKey('core_settings.ProvinceCN',
        on_delete=models.DO_NOTHING,
        limit_choices_to=models.Q(district_id=0)&~models.Q(city_id=0),
        related_name='cny_bank_city_name', verbose_name=_("Cny bank city"))

    cny_bank_mobile = models.CharField(max_length=11, verbose_name=_("Cny bank mobile"))
    override = models.BooleanField(default=False, verbose_name=_("Override"))

    def KYCRemoteValidate(self, data):
        resp = requests.post(KYC_SERVICE_HOST, data=json.dumps(four_element_data), timeout=SERVICE_REQ_TIMEOUT)
        return json.loads(r.text)

    def clean(self, *args, **kwargs):
        # Get userProfile from user_id
        userProfile = self.getProfile()
        # Get userStatus from user_id
        userStatus = self.getStatus()

        # for ROOT override
        if not self.override:
            # check real_name
            if userProfile.has_realname():
                raise ValidationError(_('user realname missing'))
            # check id_number
            if userProfile.has_id_number():
                raise ValidationError(_('user id number missing'))

            # TODO: bank account validation
            # TODO: cellphone number validation

            four_element_data = {
                'is_alien': self.getUser().is_alien,
                'real_name': userProfile.real_name,
                'id_number': userProfile.id_number,
                'bank_account': self.bank_account,
                'bank_mobile': self.cny_bank_mobile
            }

            resp = self.KYCRemoteValidate(four_element_data)

            if not resp.verified:
                raise ValidationError(_('remote validation failed'))
            else:
                # Modify KYC Status if KYC Invalid
                if not userStatus.kyc_verified:
                    userStatus.kyc_verified = True
                    userStatus.save()

        super(UserBankInfo, self).clean(*args, **kwargs)

    # Realname, country etc.
    def getProfile(self):
        try:
            return UserProfile.objects.get(user_id=self.user_id)
        except UserProfile.DoesNotExist:
            raise ValidationError(_('user profile missing'))

    # User Level / KYC etc.
    def getStatus(self):
        try:
            return UserStatus.objects.get(user_id=self.user_id)
        except UserStatus.DoesNotExist:
            raise ValidationError(_('user profile missing'))

    class Meta:
        verbose_name = _('User bank info')
        verbose_name_plural = _('User bank info')

class UserChangePwdAt(BaseModel):
    user_id = models.IntegerField(verbose_name=_("UserId"))
    change_pwd_at = models.IntegerField(verbose_name=_("ChangePwdAt"))

    class Meta:
        verbose_name = _('User change password time')
        verbose_name_plural = _('User change password times')

class UserAccessToken(BaseModel):
    user_id = models.IntegerField(verbose_name=_("UserId"))
    access_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("AccessKey"))
    secret = models.CharField(max_length=100, default=genSecret, editable=False, verbose_name=_("Secret"))
    description = models.CharField(max_length=255, blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("User access token")
        verbose_name_plural = _("User access tokens")

class UserLoginHistory(BaseModel):
    user_id = models.IntegerField(verbose_name=_("UserId"))
    ip_address = models.CharField(max_length=16, verbose_name=_("IPAddress"))
    ip_city = models.CharField(max_length=16, verbose_name=_("IPCity"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Timestamp"))

    class Meta:
        verbose_name = _('User login history')
        verbose_name_plural = _('User login histories')


class UserRequest(BaseModel):
    user_id = models.IntegerField(null=False, blank=False, verbose_name=_("UserId"))
    operator_id = models.IntegerField(null=True, blank=True, verbose_name=_("Operator Id"))
    request_type = models.SmallIntegerField(verbose_name=_("Request Type"))
    status = models.SmallIntegerField(verbose_name=_("Status"))
    data = models.CharField(max_length=255, null=False, blank=False, verbose_name=_("Data"))
    comments = models.CharField(max_length=255, null=True, blank=True, default=None, verbose_name=_("Comments"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Create at"))
    last_modify_at = models.DateTimeField(auto_now=True, verbose_name=_("Last modify at"))

    class Meta:
        verbose_name = _('User request')
        verbose_name_plural = _('User requests')
