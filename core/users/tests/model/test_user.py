from django.test import TestCase
from users.models import User

class UserTestCase(TestCase):
    def setUp(self):
    	"""
    	@China Native User
    	# No Email
    	"""
        User.objects.create(username="test_1", mobile="17721070527", user_pass="12345")
        """
        @Alien User
        # No Mobile
        """
        User.objects.create(username="test_2", email="test2@test.com", is_alien=True, user_pass="12345")

    def test_users_can_get_withdraw_status(self):
        """Users' withdrawal status are correctly identified"""
        user_cn = User.objects.get(username="test_1")
        user_alien = User.objects.get(username="test_2")
       	self.assertEqual(user_cn.getWithdrawStatus().getUser(), user_cn) 
       	self.assertEqual(user_alien.getWithdrawStatus().daily_btc_withdraw_limit, 0) 
