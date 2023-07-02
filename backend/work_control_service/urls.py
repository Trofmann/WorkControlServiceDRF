from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register('subjects', views.SubjectViewSet, basename='subjects')
router.register(r'works/subject_id/(?P<subject_id>\d+)', views.WorkViewSet, basename='works')
urlpatterns = router.urls
