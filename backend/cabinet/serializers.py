from rest_framework.serializers import ModelSerializer

from .models import ServiceUser


class ServiceUserSerializer(ModelSerializer):
    class Meta:
        model = ServiceUser
        fields = [
            'username',
        ]
