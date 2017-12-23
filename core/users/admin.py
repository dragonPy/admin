from django.contrib import admin
from users.models import *
from django.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = VaultUser
        fields = '__all__'

    def clean_email(self):
        return self.cleaned_data['email'] or None

    def clean_mobile(self):
        return self.cleaned_data['mobile'] or None


@admin.register(UserAccessToken)
class CommonAdmin(admin.ModelAdmin):
    pass


@admin.register(VaultUser)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    fields = ('user_pass_trade', )
    list_display = ('user_pass_trade', )

@admin.register(UserBankInfo)
class UserBankInfoAdmin(admin.ModelAdmin):
    fields = ('user_id', 'bank', 'cny_bank_account', 'cny_bank_name', 'cny_bank_beneficiary', 'cny_bank_province',
              'cny_bank_city', 'cny_bank_mobile', 'override')
    list_display = ('user_id', 'bank', 'cny_bank_account', 'cny_bank_name', 'cny_bank_beneficiary', 'cny_bank_province',
              'cny_bank_city', 'cny_bank_mobile', 'override')

@admin.register(UserLoginHistory)
class UserLoginHistoryAdmin(admin.ModelAdmin):
    fields = ('user_id', 'ip_address', 'ip_city')
    list_display = ('user_id', 'ip_address', 'ip_city', 'timestamp')
    readonly_fields = ('timestamp',)


@admin.register(UserConfig)
class UserConfigAdmin(admin.ModelAdmin):
    fields = ('user_id', 'name', 'value', 'modified')
    list_display = ('user_id', 'name', 'value', 'created', 'modified')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fields = ('user_id', 'real_name', 'id_number', 'id_type', 'id_type_other',
              'gender', 'country', 'state', 'birth_date', 'language', 'city', 'address', 'postal_code')
    list_display = ('user_id', 'real_name', 'id_number', 'id_type', 'id_type_other',
                    'gender', 'country', 'state', 'birth_date', 'language', 'city', 'address', 'postal_code')
    # fields=('user_id', 'real_name', 'id_number', 'id_type', 'id_type_other', 'gender', 'country')


@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    list_display = (
    'user_id', 'operator_id', 'request_type', 'status', 'data', 'comments', 'created_at', 'last_modify_at')


@admin.register(UserAuthorization)
class UserAuthorizationAdmin(admin.ModelAdmin):
    fields = ('user_id', 'user_login_attempts', 'otpkey', 'locked')
    list_display = ('user_id', 'user_login_attempts', 'otpkey', 'locked')


@admin.register(UserChangePwdAt)
class UserChangePwdAtAdmin(admin.ModelAdmin):
    fields = ('user_id', "change_pwd_at")
    list_display = ('user_id', "change_pwd_at")


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    fields = ('user_id', "phone_verified", 'email_verified', 'kyc_verified', 'id_expire_date', 'id_expire_date_verified'
              , 'id_images_status', 'compliance_lock_status', 'kyc_level', 'experience_level', "point")
    list_display = ('user_id', "phone_verified", 'email_verified', 'kyc_verified', 'id_expire_date',
                    'id_expire_date_verified', 'id_images_status', 'compliance_lock_status', 'kyc_level',
                    'experience_level', "point")


@admin.register(UserWithdrawStatus)
class UserWithdrawStatusAdmin(admin.ModelAdmin):
    fields = ('user_id', 'daily_btc_withdraw_limit', 'daily_cny_withdraw_limit', 'daily_ltc_withdraw_limit',
              'once_cny_withdraw_limit', 'max_cny_withdraw_limit', 'withdrawfeeoverride')
    list_display = ('user_id', 'daily_btc_withdraw_limit', 'daily_cny_withdraw_limit', 'daily_ltc_withdraw_limit',
                    'once_cny_withdraw_limit', 'max_cny_withdraw_limit', 'withdrawfeeoverride')
