from django.db.utils import IntegrityError
from django.test import TestCase

from cabinet.models import ServiceUser
from ...models import Subject, Work


def create_works(method):
    def wrapper(self, *args, **kwargs):
        test_subj = Subject.objects.create(name='test_subj', user=self.user)
        Work.objects.create(subject=test_subj, name='work1', status=Work.StatusType.NOT_STARTED)

        Work.objects.create(subject=test_subj, name='work2', status=Work.StatusType.IN_WORK)
        Work.objects.create(subject=test_subj, name='work3', status=Work.StatusType.IN_WORK)

        Work.objects.create(subject=test_subj, name='work4', status=Work.StatusType.COMPLETED)
        Work.objects.create(subject=test_subj, name='work5', status=Work.StatusType.COMPLETED)
        Work.objects.create(subject=test_subj, name='work6', status=Work.StatusType.COMPLETED)
        return method(self, test_subj, *args, **kwargs)

    return wrapper


class SubjectModelTest(TestCase):
    """Тест предмета"""

    def setUp(self) -> None:
        self.user = ServiceUser.objects.create(username='user')
        self.user2 = ServiceUser.objects.create(username='user2')

    def test_subject_str(self):
        """
        Тест: строковое представление предмета
        """
        subj = Subject.objects.create(name='subj', user=self.user)
        self.assertEqual(str(subj), 'subj')

    def test_ordering(self):
        """
        Тест: упорядочиваются по наименованию
        """
        subj1 = Subject.objects.create(name='c', user=self.user)
        subj2 = Subject.objects.create(name='a', user=self.user)
        subj3 = Subject.objects.create(name='b', user=self.user)

        self.assertSequenceEqual(
            list(Subject.objects.all()),
            [subj2, subj3, subj1],
        )

    def test_cant_create_subjects_with_same_names_for_one_user(self):
        """
        Тест: Один пользователь не может иметь 2 предмета с одинаковым наименованием
        """
        name = 'subj'
        Subject.objects.create(name=name, user=self.user)
        with self.assertRaises(IntegrityError):
            Subject.objects.create(name=name, user=self.user)

    def test_can_create_subjects_with_same_names_for_different_users(self):
        """
        Тест: Разные пользователи могут иметь предметы с одинаковым наименованием
        """
        name = 'subj'
        Subject.objects.create(name=name, user=self.user)
        try:
            Subject.objects.create(name=name, user=self.user2)
        except IntegrityError:
            self.fail(
                'Должна быть возможность разным пользователям иметь предметы с одинаковым наименованием'
            )

    @create_works
    def test_not_started_works_count(self, test_subj: Subject):
        """
        Тест: Правильно считается количество работ 'Не начато'
        """
        self.assertEqual(test_subj.not_started_works_count, 1)

    @create_works
    def test_in_work_works_count(self, test_subj: Subject):
        """
        Тест: правильно считается количество работ со статусом 'В работе'
        """
        self.assertEqual(test_subj.in_work_works_count, 2)

    @create_works
    def test_completed_works_count(self, test_subj: Subject):
        """
        Тест: правильно считается количество работ со статусом 'Выполнено'
        """
        self.assertEqual(test_subj.completed_works_count, 3)
