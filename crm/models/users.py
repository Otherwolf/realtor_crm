from typing import Tuple

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    phone = models.CharField(verbose_name='Телефон', max_length=16, null=False, blank=False, )
    user = models.OneToOneField(
        to=User,
        verbose_name='Пользователь',
        related_name='profile',
        on_delete=models.CASCADE,
        null=True, blank=False
    )

    class Meta:
        verbose_name: str = 'Профиль пользователя'
        verbose_name_plural: str = 'Профили пользователей'
        ordering: Tuple[str, ...] = ('user__last_name',)

    def __str__(self) -> str:
        user_name_list = []
        if self.user.first_name != '':
            user_name_list.append(self.user.first_name)
        if self.user.last_name != '':
            user_name_list.append(self.user.last_name)
        return ' '.join(user_name_list)


__all__ = ('UserProfile',)
