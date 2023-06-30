from django.urls import re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('subjects', views.SubjectViewSet, basename='subjects')
router.register('works', views.WorkViewSet, basename='works')
urlpatterns = router.urls

urlpatterns += [
    re_path(r'works/subject_id/(?P<subject_id>\d+)', views.WorkViewSet.as_view({'get': 'list'}))
]

