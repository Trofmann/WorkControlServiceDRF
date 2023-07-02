from rest_framework.viewsets import ModelViewSet

from ..models import Work, Subject
from ..permissions import IsWorkOwner
from ..serializers import WorkSerializer

__all__ = [
    'WorkViewSet',
]


class WorkViewSet(ModelViewSet):
    serializer_class = WorkSerializer
    permission_classes = [IsWorkOwner]

    @property
    def subject(self):
        subject_id = self.kwargs['subject_id']
        return Subject.objects.filter(user=self.request.user, pk=subject_id).first()

    def get_queryset(self):
        return Work.objects.filter(subject__user=self.request.user, subject=self.subject)

    def perform_create(self, serializer):
        serializer.save(subject=self.subject)
