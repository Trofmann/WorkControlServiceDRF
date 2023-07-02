from datetime import datetime
from django.utils.timezone import now

from django.db import models

__all__ = [
    'Work'
]


class Work(models.Model):
    """Работа по предмету"""

    class StatusType(models.TextChoices):
        NOT_STARTED = 1, 'Не начато'
        IN_WORK = 2, 'В работе'
        COMPLETED = 3, 'Выполнено'

    subject = models.ForeignKey(
        to='work_control_service.Subject',
        verbose_name='Предмет',
        related_name='works',
        on_delete=models.CASCADE,
        null=False, blank=False,
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        null=False, blank=False,
    )
    deadline = models.DateField(
        verbose_name='Дедлайн',
        null=True, blank=True,
    )
    status = models.CharField(
        verbose_name='Статус',
        choices=StatusType.choices,
        null=False, blank=False,
        max_length=1024,
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'
        ordering = ['deadline', 'status', 'name']
        unique_together = ('subject', 'name')

    def __str__(self):
        return self.name

    @property
    def expired(self):
        if self.deadline:
            today = now().date()
            return not self.completed and (today > self.deadline)
        return False

    @property
    def completed(self):
        return self.status == self.StatusType.COMPLETED
