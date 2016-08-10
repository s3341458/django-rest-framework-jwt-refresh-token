from django.conf.urls import url

from refreshtoken.views import DelegateJSONWebToken

from refreshtoken.routers import router


urlpatterns = router.urls + [
    url(r'^delegate/$', DelegateJSONWebToken.as_view(),
        name='delegate-tokens'),
]
