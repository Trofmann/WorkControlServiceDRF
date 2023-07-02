from rest_framework.serializers import ModelSerializer

from ..models import Work

__all__ = [
    'WorkSerializer'
]


class WorkSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = [
            'id',
            'name',
            'deadline',
            'status',
            'comment',
        ]
