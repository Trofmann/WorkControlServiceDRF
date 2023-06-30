from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import ServiceUser
from .serializers import ServiceUserSerializer


class ServiceUsersViewSet(ModelViewSet):
    serializer_class = ServiceUserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ServiceUser.objects.all()
