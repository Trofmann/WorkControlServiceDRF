from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase, APIRequestFactory

from cabinet.models import ServiceUser
from ...models import Subject
from ...serializers import SubjectSerializer

factory = APIRequestFactory()


class SubjectViewSetTest(APITestCase):
    """Тест представления предметов"""

    def setUp(self):
        self.staff_user = ServiceUser.objects.create_user(username='staff_user', is_staff=True)
        self.client.force_authenticate(self.staff_user)

    def test_available_by_url(self):
        """
        Тест: доступно по url
        """
        response = self.client.get(reverse('subjects-list'))
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_returns_right_queryset(self):
        """
        Тест: возвращает правильный queryset
        """
        right_user = self.staff_user
        subj1 = Subject.objects.create(name='subj1', user=right_user)
        subj2 = Subject.objects.create(name='subj2', user=right_user)

        other_user = ServiceUser.objects.create_user(username='other_user')
        Subject.objects.create(name='subj1', user=other_user)
        Subject.objects.create(name='subj2', user=other_user)

        response = self.client.get(reverse('subjects-list'))
        expected_data = SubjectSerializer([subj1, subj2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_create_for_user(self):
        """
        Тест: создаётся предмет для пользователя
        """
        data = {'name': 'subj1'}
        self.client.post(reverse('subjects-list'), data=data)
        self.assertQuerysetEqual(Subject.objects.all(), self.staff_user.subjects.all())
