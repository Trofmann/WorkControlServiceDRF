from rest_framework import routers

from . import views

app_name = 'cabinet'

routers = routers.DefaultRouter()
routers.register('users', views.ServiceUsersViewSet, basename='users')

urlpatterns = routers.urls
