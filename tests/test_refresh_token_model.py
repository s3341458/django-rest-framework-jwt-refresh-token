import datetime as dt

import pytest
from django.utils import timezone


def test_revocation(refresh_token, alice):
    from refreshtoken.models import RefreshToken

    new_refresh_token = refresh_token.revoke()
    assert new_refresh_token.key != refresh_token.key
    assert new_refresh_token.user == alice
    assert new_refresh_token.app == 'refresh_token'
    with pytest.raises(RefreshToken.DoesNotExist):
        refresh_token.refresh_from_db()


def test_repr(alice):
    from refreshtoken.models import RefreshToken

    assert repr(RefreshToken()) == (
        "RefreshToken(pk='', key='', user=None, app='', created=None)")
    refresh_token = RefreshToken(user=alice, app='local', key='foo')
    refresh_token.save()
    now = dt.datetime.utcnow().replace(tzinfo=timezone.get_default_timezone())
    refresh_token.created = now
    assert repr(refresh_token) == (
        "RefreshToken(pk=%r, key='foo', user=%r, app='local', created=%r)" % (
            refresh_token.pk,
            alice,
            now,
        ))
