from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APITestCase, force_authenticate

from ..models import ServiceUser


class ServiceUsersViewSetTest(APITestCase):
    """
    Тест списка пользователей
    """
    url = reverse('cabinet:users-list')

    def setUp(self):
        self.staff_user = ServiceUser.objects.create_user(username='staff_user', is_staff=True)
        self.common_user = ServiceUser.objects.create_user(username='common_user')

    def test_available_by_url(self):
        """
        Доступно по url
        """
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_can_create_user(self):
        """
        Тест: можно создать пользователя
        """
        self.client.force_authenticate(self.staff_user)
        data = {'username': 'test_user'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(ServiceUser.objects.count(), 3)
