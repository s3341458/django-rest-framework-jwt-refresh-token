from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from refreshtoken.models import RefreshToken

User = get_user_model()


class AdminTest(TestCase):
    def setUp(cls):
        test_users_info = [
            ('a@example.com', 'usera', 'passworda')
            ('b@example.com', 'userb', 'passwordb')
            ('c@example.com', 'userc', 'passwordc')
        ]
        for user_info in test_users_info:
            user = User.objects.create_user(*user_info)
            user.is_superuser = True
            user.save()
            RefreshToken.objects.create(user=user, app='test-app')

        cls.client = Client()

        cls.admin_url = '/admin/refreshtoken/refreshtoken'

    def test_refresh_token_admin_exists(self):
        self.client.login(username='usera', password='passworda')
        response = self.client.get(self.admin_url, follow=True)
        self.assertEqual(response.status_code, 200,
                         'Failed to visit business user change field')
