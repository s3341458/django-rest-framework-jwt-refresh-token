import pytest


def test_revocation(refresh_token, alice):
    from refreshtoken.models import RefreshToken

    new_refresh_token = refresh_token.revoke()
    assert new_refresh_token.key != refresh_token.key
    assert new_refresh_token.user == alice
    assert new_refresh_token.app == 'refresh_token'
    with pytest.raises(RefreshToken.DoesNotExist):
        refresh_token.refresh_from_db()
