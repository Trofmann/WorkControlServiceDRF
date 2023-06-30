from rest_framework.serializers import ModelSerializer

from ..models import Subject

__all__ = [
    'SubjectSerializer',
]


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'id',
            'name',
            'comment',
            'not_started_works_count',
            'in_work_works_count',
            'completed_works_count',
            'user_id',
        ]
