from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'tuitionposts', TuitionPostViewSet)
router.register(r'blogcomments', BlogCommentViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'classes', ClassesViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'subdistricts', SubDistrictViewSet)
router.register(r'notifications', NotificationViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
