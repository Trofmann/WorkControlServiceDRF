from rest_framework.test import APITestCase
from django.test import RequestFactory

from cabinet.models import ServiceUser
from ...models import Subject, Work
from ...permissions import IsWorkOwner


class IsWorkOwnerPermissionTest(APITestCase):
    """Тест разрешения для работы"""

    def setUp(self):
        self.correct_user = ServiceUser.objects.create(username='correct')
        self.other_user = ServiceUser.objects.create(username='other')

        self.subject = Subject.objects.create(name='subj', user=self.correct_user)
        self.work = Work.objects.create(
            subject=self.subject,
            name='work',
            status=Work.StatusType.NOT_STARTED
        )

    def test_subject_owner_has_permission_to_work(self):
        """
        Тест: Владелец предмета может получить доступ к работе
        """
        factory = RequestFactory()

        request = factory.get('/')
        request.user = self.correct_user

        permission = IsWorkOwner()
        self.assertTrue(permission.has_object_permission(request, None, self.work))

    def test_not_subject_owner_doesnt_have_permission_to_work(self):
        """
        Тест: не владелец не может получить доступ к работе
        """
        factory = RequestFactory()

        request = factory.get('/')
        request.user = self.other_user

        permission = IsWorkOwner()
        self.assertFalse(permission.has_object_permission(request, None, self.work))
