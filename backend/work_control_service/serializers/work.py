from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from ..models import Work, Subject

__all__ = [
    'WorkSerializer'
]


class WorkSerializer(ModelSerializer):
    subject = PrimaryKeyRelatedField(queryset=Subject.objects.none())

    class Meta:
        model = Work
        fields = [
            'id',
            'subject',
            'name',
            'deadline',
            'status',
            'comment',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(user=self.context['request'].user)
