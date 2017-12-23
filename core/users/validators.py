from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

USER_CONF_KEYS = [
    'verified_auto_deposit',        # Alpha Test User
    'twofactor_trade',              # 2Factor Condition
    'twofactor_withdraw',           # 
    'twofactor_login',
    'disable_txpassword_trade',
    'kyc_error',                    # KYC_Error Reason
    'kyc_validate_count',
    'lock_comment',                 #
    'withdraw_lock_comment',        # 
    'withdraw_lock_margin',         # lock withdraw because user has open margin
    'withdraw_default_btc_addr',    # default BTC withdrawl address 
    'withdraw_default_ltc_addr',    # default LTC withdrawl address
]

def validate_user_config(value):
    if not value in USER_CONF_KEYS:
        raise ValidationError(
            _('%(value)s is not a valid config key'),
            params={ 'value': value },
        
        )