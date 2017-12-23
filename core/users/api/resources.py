from tastypie.resources import ModelResource, ALL
from tastypie.authorization import Authorization
from users.models import *


class UserRequestResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = UserRequest.objects.all()
        authorization = Authorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']


class UserResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = User.objects.all()
        authorization = Authorization()
        list_allowed_methods = ['get', 'post', 'put']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
            'email': ALL,
            'mobile': ALL,
            'username': ALL
        }


class UserWithdrawStatusResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = UserWithdrawStatus.objects.all()
        authorization = Authorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        filtering = {
            'user_id': ALL
        }


class UserLoginHistoryResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = UserLoginHistory.objects.all()
        authorization = Authorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
            'user_id': ALL
        }


class UserBankInfoResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = UserBankInfo.objects.all()
        authorization = Authorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put']
        filtering = {
            'user_id': ALL
        }



class UserAuthorizationResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = UserAuthorization.objects.all()
        authorization = Authorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put']
        filtering = {
            'user_id': ALL
        }


class UserProfileResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = UserProfile.objects.all()
        authorization = Authorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post','put']
        filtering = {
            'user_id': ALL
        }


class UserStatusResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = UserStatus.objects.all()
        authorization = Authorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post' , 'put']
        filtering = {
            'user_id': ALL
        }


class UserChangePwdAtResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = UserChangePwdAt.objects.all()
        authorization = Authorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
            'user_id': ALL
        }


class UserAccessKeyResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = UserAccessToken.objects.all()
        authorization = Authorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'delete']
        filtering = {
            'user_id': ALL
        }


class UserConfigResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = UserConfig.objects.all()
        authorization = Authorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put']
        filtering = {
            'user_id': ALL,
            'name': ALL
        }
