from django.conf import settings
from django.db import models

from work_control_service.models import Work

__all__ = [
    'Subject',
]


class Subject(models.Model):
    """Предмет"""
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        null=False, blank=False
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        related_name='subjects',
        null=False, blank=False,
        on_delete=models.CASCADE,
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['name']
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name

    def get_status_works_count(self, status):
        return self.works.filter(status=status).count()

    @property
    def not_started_works_count(self) -> int:
        return self.get_status_works_count(status=Work.StatusType.NOT_STARTED)

    @property
    def in_work_works_count(self):
        return self.get_status_works_count(status=Work.StatusType.IN_WORK)

    @property
    def completed_works_count(self):
        return self.get_status_works_count(status=Work.StatusType.COMPLETED)
