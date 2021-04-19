from typing import Tuple

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Developer(models.Model):
    updated_at = models.DateTimeField(auto_now=True, null=False, verbose_name='Дата изменения')
    created_at = models.CharField(null=True, default='', blank=True, verbose_name='Дата основания', max_length=64)
    description = models.TextField(verbose_name='Описание', blank=True, null=False, default='', max_length=2048)
    objects_delivered = models.IntegerField(verbose_name='Сдано объектов', blank=False, null=True)
    objects_under_construction = models.IntegerField(verbose_name='Объектов строится', blank=False, null=True)
    updated_by = models.ForeignKey(
        to=User,
        verbose_name='Кем изменена',
        on_delete=models.SET_NULL,
        null=True
    )
    name = models.CharField(
        verbose_name='Наименование',
        unique=True,
        max_length=128,
        default='',
        blank=False, null=False,
    )

    class Meta:
        verbose_name: str = 'Застройщик'
        verbose_name_plural: str = 'Застройщики'
        ordering: Tuple[str, ...] = ('name',)

    def __str__(self) -> str:
        return self.name

    @property
    def count_complexes(self) -> int:
        return self.complexes.all().count()


__all__ = ('Developer',)
