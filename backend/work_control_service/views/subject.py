from rest_framework.viewsets import ModelViewSet

from ..models import Subject
from ..serializers import SubjectSerializer
from ..permissions import IsSubjectOwner

__all__ = [
    'SubjectViewSet',
]


class SubjectViewSet(ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [IsSubjectOwner]

    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
