def test_is_admin_or_owner_permission(refresh_token, admin_user, mocker,
                                      alice):
    from refreshtoken.permissions import IsOwnerOrAdmin

    request = mocker.Mock()
    anonymous_user = mocker.Mock()
    anonymous_user.is_authenticated = False
    request.user = anonymous_user

    backend = IsOwnerOrAdmin()
    assert not backend.has_permission(request, None)
    assert not backend.has_object_permission(request, None, refresh_token)

    request.user = admin_user
    assert backend.has_permission(request, None)

    assert backend.has_object_permission(request, None, refresh_token)

    request.user = alice
    assert backend.has_object_permission(request, None, refresh_token)
