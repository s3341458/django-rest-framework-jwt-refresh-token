from django_webtest import WebTest
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model

from refreshtoken.models import RefreshToken
from refreshtoken.admin import RefreshTokenAdmin, revoke_refresh_tokens

User = get_user_model()


class MockRequest:
    def __init__(self, user=None):
        self.user = user


class AdminSiteTest(WebTest):
    def setUp(self):
        self.password = 'arandompassword'
        test_users_info = [
            ('a@example.com', 'usera', self.password),
            ('b@example.com', 'userb', self.password),
            ('c@example.com', 'userc', self.password),
        ]

        self.users = []

        for user_info in test_users_info:
            user = User.objects.create_user(*user_info)
            user.is_superuser = True
            user.save()
            self.users.append(user)
            RefreshToken.objects.create(user=user, app='test-app')

        self.admin = RefreshTokenAdmin(
            model=RefreshToken, admin_site=AdminSite()
        )
        self.request = MockRequest(self.users[0])

    def test_refresh_token_admin_fields(self):
        self.assertEqual(
            self.admin.get_fields(self.request),
            ['user', 'key', 'app'],
            'All fields are user, key, app'
        )
        self.assertEqual(
            self.admin.get_list_display(self.request),
            ['user', 'key'],
            'Only user and key should be in list fields'
        )
        self.assertEqual(
            self.admin.readonly_fields,
            ['user', 'key', 'app'],
            'All refresh_token fields in admin should all be readonly'
        )

    def test_self_admin_actions(self):
        refresh_token = RefreshToken(user=self.users[0], app='local')
        refresh_token.save()
        previous_token = refresh_token.key
        revoke_refresh_tokens(
            self.admin, self.request,
            RefreshToken.objects.filter(user=self.users[0])
        )
        refresh_token = RefreshToken.objects.filter(user=self.users[0]).first()
        self.assertNotEqual(
            previous_token, refresh_token.key,
            'Refresh tokens did not revoked after revoke action'
        )
