from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from tastypie.models import create_api_key
from users.models import VaultUser, UserWithdrawStatus, UserBankInfo, UserAuthorization, UserProfile, UserStatus

@receiver(post_save, sender=User)
def create_user_profile_and_apikey(sender, instance, created, **kwargs):
    if instance.is_superuser:
        return
    if created:
        VaultUser.objects.create(
            user=instance, 
        )
        create_api_key(User, instance=instance, created=True)

# Initialize Other User tables when user is created in the user table
@receiver(post_save, sender=VaultUser, dispatch_uid="user_create")
def initializeUserTables(sender, instance, **kwargs):
    UserWithdrawStatus.objects.get_or_create(user_id=instance.id)
    UserAuthorization.objects.get_or_create(user_id=instance.id)
    UserStatus.objects.get_or_create(user_id=instance.id)
    try:
        obj = UserProfile.objects.get(user_id=instance.id)
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user_id=instance.id, country=None)