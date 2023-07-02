from datetime import timedelta, date
from random import choice

from django.test import TestCase
from django.utils.timezone import now
from django.db.utils import IntegrityError

from cabinet.models import ServiceUser
from ...models import Subject, Work


class WorkModelTest(TestCase):
    """Тест модели работы"""

    def setUp(self) -> None:
        user = ServiceUser.objects.create_user(username='user')
        self.subject = Subject.objects.create(user=user, name='subj')
        self.work_statuses = [Work.StatusType.NOT_STARTED, Work.StatusType.IN_WORK, Work.StatusType.COMPLETED]
        self.work_statuses_not_completed = [Work.StatusType.NOT_STARTED, Work.StatusType.IN_WORK]
        self.today = now().date()

    def create_not_completed_work(self, deadline: date, name='work') -> Work:
        """
        Создание невыполненной работы
        """
        status = choice(self.work_statuses_not_completed)
        work = Work.objects.create(
            subject=self.subject,
            name='work',
            status=status,
            deadline=deadline,
        )
        return work

    def test_work_str(self):
        """
        Тест: строковое представление работы
        """
        work = Work.objects.create(subject=self.subject, name='work', status=Work.StatusType.NOT_STARTED)
        self.assertEqual(str(work), 'work')

    def test_ordering(self):
        """
        Тест: правильный порядок (дедлайн, статус, наименование)
        """
        # Должны отсортироваться по наименованию и стоять в конце
        work1 = Work.objects.create(
            subject=self.subject,
            name='work_y',
            status=Work.StatusType.COMPLETED,
            deadline=self.today + timedelta(days=50)
        )  # Самое 'Большое' название и самый поздний дедлайн
        work2 = Work.objects.create(
            subject=self.subject,
            name='work_a',
            status=Work.StatusType.COMPLETED,
            deadline=self.today + timedelta(days=50)
        )  # Самый поздний дедлайн

        # Должен Отсортироваться по дедлайну и стоять в начале
        work3 = Work.objects.create(
            subject=self.subject,
            name='work_e',
            status=Work.StatusType.NOT_STARTED,
            deadline=self.today - timedelta(days=100)
        )  # Самый ранний дедлайн

        # Должны отсортироваться по статусу
        work4 = Work.objects.create(
            subject=self.subject,
            name='work_b',
            status=Work.StatusType.NOT_STARTED,
            deadline=self.today,
        )
        work5 = Work.objects.create(
            subject=self.subject,
            name='work_d',
            status=Work.StatusType.IN_WORK,
            deadline=self.today,
        )
        expected_sequence = [work3, work4, work5, work2, work1]
        self.assertSequenceEqual(list(Work.objects.filter(subject=self.subject)), expected_sequence)

    def test_cant_create_works_with_same_names_for_one_subject(self):
        """
        Тест: для одного предмета нельзя создать несколько работ с одинаковым наименованием
        """
        name = 'work'
        Work.objects.create(subject=self.subject, name=name, status=Work.StatusType.NOT_STARTED)
        with self.assertRaises(IntegrityError):
            Work.objects.create(subject=self.subject, name=name, status=Work.StatusType.IN_WORK)

    def test_work_without_deadline_is_not_expired(self):
        """
        Тест: работа без указанного дедлайна не просрочена
        """
        status = choice(self.work_statuses)
        work = Work.objects.create(
            subject=self.subject,
            name='work',
            status=status
        )
        self.assertFalse(work.expired)

    def test_completed_work_is_not_expired(self):
        """
        Тест: выполненная работа не просрочена
        """
        deadline = self.today - timedelta(days=10)
        work = Work.objects.create(
            subject=self.subject,
            name='work',
            status=Work.StatusType.COMPLETED,
            deadline=deadline,
        )
        self.assertFalse(work.expired)

    def test_not_completed_work_with_deadline_later_then_today_is_not_expired(self):
        """
        Тест: невыполненная работа с дедлайном позже, чем сегодня не просрочена
        """
        deadline = self.today + timedelta(days=10)
        work = self.create_not_completed_work(deadline)
        self.assertFalse(work.expired)

    def test_work_with_deadline_equal_today_is_not_expired(self):
        """
        Тест: работа с дедлайном сегодня - просрочена
        """
        deadline = self.today
        work = self.create_not_completed_work(deadline)
        self.assertFalse(work.expired)

    def test_work_with_deadline_earlier_then_today_is_expired(self):
        """
        Тест: работа с дедлайном раньше, чем сегодня - просрочена
        """
        deadline = self.today - timedelta(days=10)
        work = self.create_not_completed_work(deadline)
        self.assertTrue(work.expired)

    def test_completed_property(self):
        """
        Тест: свойство completed смотрит на правильный статус
        """
        work = Work.objects.create(
            subject=self.subject,
            name='work',
            status=Work.StatusType.COMPLETED,
        )
        self.assertTrue(work.completed)
