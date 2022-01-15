from django.urls import path

from rest_framework.routers import DefaultRouter

from .views.user_views import UserViewSet, GroupsViewSet
from .views.rfi_views import RfiViewSet, AttachmentViewSet
from .views.response_views import ResponseViewSet
from .views.job_views import JobViewSet

router = DefaultRouter()
router.register("rfi", RfiViewSet, basename="rfis")
router.register("response", ResponseViewSet, basename="responses")
router.register("attachment", AttachmentViewSet, basename="attachments")
router.register("user", UserViewSet, basename="users")
router.register("group", GroupsViewSet, basename="groups")
router.register("job", JobViewSet, basename="jobs")

urlpatterns = router.urls
