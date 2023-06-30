from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from ..models import Work
from ..serializers import WorkSerializer
from ..permissions import IsWorkOwner

__all__ = [
    'WorkViewSet',
]


class WorkViewSet(ModelViewSet):
    serializer_class = WorkSerializer
    permission_classes = [IsWorkOwner]

    def get_queryset(self):
        return Work.objects.filter(subject__user=self.request.user)

    def list(self, request, *args, **kwargs):
        subject_id = kwargs.get('subject_id', None)

        if subject_id:
            queryset = Work.objects.filter(subject_id=subject_id)
        else:
            queryset = Work.objects.none()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
