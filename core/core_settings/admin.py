from django.contrib import admin
from core_settings.models import *

@admin.register(PointLevel)
class PointLevelAdmin(admin.ModelAdmin):
    fields=('level', 'level_str', 'point_upper', 'point_lower', 'withdraw_rate', 'loan_leverage')
    list_display=('level_str', 'level', 'point_upper', 'point_lower', 'withdraw_rate', 'loan_leverage')

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    fields=('code', 'name_str_cn', 'card_length_enterprise', 'card_length_private')
    list_display=('code', 'name_str_cn', 'card_length_enterprise', 'card_length_private')

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fields=('name', 'name_en', 'iso2', 'mobile_code')
    list_display=('name', 'name_en', 'iso2', 'mobile_code')

@admin.register(FundLimit)
class FundLimitAdmin(admin.ModelAdmin):
    fields=('span', 'currency', 'withdraw', 'deposit', 'memo')
    list_display=('memo', 'currency', 'withdraw', 'deposit', 'span')
    ordering = ('memo',)

@admin.register(ProvinceCN)
class ProvinceCNAdmin(admin.ModelAdmin):
    fields=('district_id', 'district_name', 'city_id', 'city_name', 'province_id', 'province_name')
    list_display=('district_id', 'district_name', 'city_id', 'city_name', 'province_id', 'province_name')

@admin.register(KYCLevel)
class KYCLevelAdmin(admin.ModelAdmin):
    fields=('condition', 'level', 'alien', 'limits')
    list_display=('condition', 'level', 'alien')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    fields=('alpha2', 'alpha3b', 'english')
    list_display=('alpha2', 'alpha3b', 'english')
