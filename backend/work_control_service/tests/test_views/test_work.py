from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APITestCase

from cabinet.models import ServiceUser
from ...models import Subject, Work
from ...serializers import WorkSerializer


class WorkViewSetTest(APITestCase):
    """Тест представления работы"""

    def setUp(self) -> None:
        self.user = ServiceUser.objects.create(username='user')
        self.subject = Subject.objects.create(user=self.user, name='subj')
        self.client.force_authenticate(self.user)
        self.list_url = reverse('works-list', kwargs={'subject_id': self.subject.id})

    def test_available_by_url(self):
        """
        Тест: доступно по url
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_returns_right_query_set(self):
        """
        Тест: возвращает правильный queryset
        """
        right_subject = self.subject
        work1 = Work.objects.create(subject=right_subject, name='work1', status=Work.StatusType.NOT_STARTED)
        work2 = Work.objects.create(subject=right_subject, name='work2', status=Work.StatusType.NOT_STARTED)

        other_subject = Subject.objects.create(user=self.user, name='other')
        Work.objects.create(subject=other_subject, name='work1', status=Work.StatusType.NOT_STARTED)
        Work.objects.create(subject=other_subject, name='work2', status=Work.StatusType.NOT_STARTED)

        response = self.client.get(self.list_url)
        expected_data = WorkSerializer([work1, work2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_create_for_subject(self):
        """
        Тест: работа создаётся с правильным предметом
        """
        data = {
            'name': 'work1',
            'status': Work.StatusType.NOT_STARTED,
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertQuerysetEqual(Work.objects.all(), self.subject.works.all())
