from django.contrib.auth.models import AbstractUser


class ServiceUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        ordering = ('id',)
