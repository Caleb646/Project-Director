from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import InviteTokenViewSet, AuthViewSet, JWTTokenRefresh 

router = DefaultRouter()
router.register("invite-token", InviteTokenViewSet, basename="invite-tokens")
#url: /api/auth/user/login/ or /api/auth/user/logout/
router.register("user", AuthViewSet, basename="users")

urlpatterns = [
    #path('me/', WhoAmI.as_view(), name="who-am-i"),
    path('token/refresh/', JWTTokenRefresh.as_view(), name="refresh"),
] + router.urls