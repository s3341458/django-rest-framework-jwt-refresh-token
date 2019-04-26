from .models import RefreshToken

from django.contrib import admin
from django.conf import settings


# Prior to Django 1.5, the AUTH_USER_MODEL setting does not exist.
# Note that we don't perform this code in the compat module due to
# bug report #1297
# See: https://github.com/tomchristie/django-rest-framework/issues/1297
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


def revoke_refresh_tokens(modelAdmin, request, queryset):
    for token in queryset:
        token.revoke()


revoke_refresh_tokens.short_description = 'Revoke selected tokens'


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    readonly_fields = ['user', 'key', 'app']
    list_display = ['user', 'key']
    actions = [revoke_refresh_tokens, ]

    ordering = search_fields = ['user__' + AUTH_USER_MODEL.USERNAME_FIELD]
