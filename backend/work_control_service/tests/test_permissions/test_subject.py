from django.test import RequestFactory
from rest_framework.test import APITestCase

from cabinet.models import ServiceUser
from ...models import Subject
from ...permissions import IsSubjectOwner


class IsSubjectOwnerPermissionTest(APITestCase):
    """Тест разрешения для предмета"""

    def setUp(self):
        self.correct_user = ServiceUser.objects.create(username='correct')
        self.other_user = ServiceUser.objects.create(username='other')
        self.subject = Subject(name='subj', user=self.correct_user)

    def test_owner_has_permission_to_subject(self):
        """
        Тест: владелец может получить доступ к предмету
        """
        factory = RequestFactory()

        request = factory.get('/')
        request.user = self.correct_user

        permission = IsSubjectOwner()

        self.assertTrue(permission.has_object_permission(request, None, self.subject))

    def test_not_owner_doesnt_have_permission_to_subject(self):
        """
        Тест: не владелец не может получить доступ к предмету
        """
        factory = RequestFactory()

        request = factory.get('/')
        request.user = self.other_user

        permission = IsSubjectOwner()
        self.assertFalse(permission.has_object_permission(request, None, self.subject))
