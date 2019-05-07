from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase

from refreshtoken.models import RefreshToken
from refreshtoken.admin import RefreshTokenAdmin, revoke_refresh_tokens

User = get_user_model()


class MockRequest:
    def __init__(self, user=None):
        self.user = user


class AdminSiteTest(TestCase):
    def setUp(self):
        self.password = 'arandompassword'

        user = User.objects.create_user(
            'admin@example.com', 'user', self.password
        )
        user.is_superuser = True
        user.save()
        self.user = user
        RefreshToken.objects.create(user=user, app='test-app')

        self.admin = RefreshTokenAdmin(
            model=RefreshToken, admin_site=AdminSite()
        )
        self.request = MockRequest(self.user)

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

    def test_admin_has_token_revoke_action(self):
        self.assertEqual(self.admin.actions, [revoke_refresh_tokens])

    def test_admin_token_revoke_action(self):
        refresh_token = RefreshToken(user=self.user, app='local')
        refresh_token.save()
        previous_token = refresh_token.key
        revoke_refresh_tokens(
            self.admin, self.request,
            RefreshToken.objects.filter(user=self.user)
        )
        refresh_token = RefreshToken.objects.filter(user=self.user).first()
        self.assertNotEqual(
            previous_token, refresh_token.key,
            'Refresh tokens did not revoked after revoke action'
        )
