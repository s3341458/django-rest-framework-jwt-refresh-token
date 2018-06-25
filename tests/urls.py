from django.conf.urls import url

from refreshtoken.routers import router
from refreshtoken.views import DelegateJSONWebToken

urlpatterns = router.urls + [
    url(r'^delegate/$', DelegateJSONWebToken.as_view(),
        name='delegate-tokens'),
]
