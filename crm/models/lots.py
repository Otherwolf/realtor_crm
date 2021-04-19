import datetime
import os
from typing import (List, Tuple, Union)

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.datetime_safe import date
from django.utils.html import mark_safe

from crm.consts import (VIEW_FROM_WINDOWS, NAME_TYPE_ROOMS)
from crm.utils.base import images_upload_path

User = get_user_model()


class Lot(models.Model):
    SOLD_LOST_STATUS: str = 'Продано'
    FREE_LOST_STATUS: str = 'Свободно'
    RESERVATION_LOST_STATUS: str = 'Забронировано'

    LOT_STATUSES: List[Tuple[str, str]] = [
        (SOLD_LOST_STATUS, 'Продано'),
        (RESERVATION_LOST_STATUS, 'Забронировано'),
        (FREE_LOST_STATUS, 'Свободно'),
    ]

    updated_at = models.DateTimeField(auto_now=True, null=False, verbose_name='Дата изменения')
    n_on_price = models.CharField(verbose_name='№ по прайсу', default='', max_length=64, null=False, blank=True, )
    floor = models.IntegerField(verbose_name='Этаж', blank=True, null=False, default=0)
    s = models.FloatField(verbose_name='Площадь', null=False, blank=False, default=0)
    trim = models.CharField(verbose_name='Отделка', null=False, blank=False, max_length=32)
    options = models.TextField(verbose_name='Опции', null=False, blank=True, default='')
    reward = models.FloatField(verbose_name='Вознаграждение', null=True, blank=True)
    currency = models.CharField(verbose_name='Цена в валюте', null=False, blank=True, default='', max_length=32)
    price = models.FloatField(verbose_name='Цена в руб.', null=False, blank=False, default=0)
    comment = models.TextField(verbose_name='Комментарий', null=False, blank=True, default='')

    status = models.CharField(
        verbose_name='Статус',
        choices=LOT_STATUSES,
        max_length=128,
        default=FREE_LOST_STATUS,
        blank=False, null=False,
    )
    # Лот
    name = models.CharField(
        verbose_name='Наименование',
        max_length=252,
        choices=NAME_TYPE_ROOMS,
        null=False, blank=True,
    )
    type_object = models.ForeignKey(
        to='crm.PremisesType',
        verbose_name='Тип объекта',
        on_delete=models.SET_NULL,
        null=True,
    )
    view_from_windows = models.CharField(
        verbose_name='Вид из окон',
        choices=VIEW_FROM_WINDOWS,
        max_length=32,
        null=False, blank=False,
    )
    plan = models.ForeignKey(
        to='crm.Plan',
        verbose_name='План помещения',
        null=True, blank=True,
        default='',
        on_delete=models.DO_NOTHING
    )
    updated_by = models.ForeignKey(
        to=User,
        verbose_name='Кем изменена',
        on_delete=models.DO_NOTHING,
        blank=False, null=False
    )

    def __str__(self) -> str:
        price = '{:,}'.format(int(self.price)).replace(',', ' ')
        end = ', {0} м² за {1}₽'.format(int(self.s), price)
        if 'вартир' in self.type_object.name or 'партамент' in self.type_object.name:
            return '{0} {1}{2}'.format(self.type_object.name, self.name, end)
        return self.type_object.name + end

    @property
    def url_plan(self) -> str:
        if self.plan:
            return self.plan.plan.url
        return ''

    @property
    def price_per_m(self):
        if self.s and self.price:
            try:
                return self.price / self.s
            except ZeroDivisionError:
                pass
        return ''

    @property
    def currency_per_m(self):
        if self.s and self.currency:
            try:
                return self.currency / self.s
            except ZeroDivisionError:
                pass
        return ''


class Plan(models.Model):
    name = models.CharField(verbose_name='Название', null=True, blank=False, default='', max_length=64)
    updated_at = models.DateTimeField(auto_now=True, null=False, verbose_name='Дата изменения')
    plan = models.ImageField(upload_to=images_upload_path, null=False, verbose_name='План')
    plan_floor = models.ForeignKey(
        to='crm.Floor',
        verbose_name='Планировка этажа',
        related_name='floors',
        null=True, blank=True,
        on_delete=models.DO_NOTHING
    )
    updated_by = models.ForeignKey(
        to=User,
        verbose_name='Кем изменена',
        on_delete=models.DO_NOTHING,
        blank=False, null=False
    )

    class Meta:
        verbose_name: str = 'План помещения'
        verbose_name_plural: str = 'Планы помещений'

    def __str__(self) -> str:
        return self.name or f'{self.id}'

    @property
    def get_size(self) -> str:
        """Размер"""
        if os.path.exists(self.plan.path):
            return "%0.1f KB" % (os.path.getsize(self.plan.path) / 1024.0)
        return "0 MB"

    @property
    def get_created_at(self) -> Union[str, date]:
        """Дата загрузки"""
        if os.path.exists(self.plan.path):
            statbuf = os.stat(self.plan.path)
            return datetime.datetime.utcfromtimestamp(statbuf.st_ctime).date()
        return ''

    def image_tag(self) -> str:
        """Image"""
        if self.plan:
            return mark_safe(f'<img src="/media/{self.plan}" width="350" height="auto" />')
        return 'Изображение отсутствует'


class NewBuildingLot(Lot):
    lease = models.CharField(verbose_name='Сдача', null=False, blank=True, default='', max_length=128)
    corp = models.ForeignKey(
        to='crm.Corp',
        verbose_name='Корпус',
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
    complex = models.ForeignKey(
        to='crm.Complex',
        verbose_name='ЖК',
        on_delete=models.CASCADE,
        related_name='new_buildings',
        null=True, blank=True,
    )

    class Meta:
        verbose_name: str = 'Новостройка'
        verbose_name_plural: str = 'Новостройки'

    @property
    def type_building(self) -> str:
        return 'newbuildinglot'

    @property
    def corp_name(self) -> str:
        if self.corp:
            return self.corp.name
        return ''


class OldBuildingLot(Lot):
    lease = models.CharField(verbose_name='Сдача', null=False, blank=True, default='', max_length=128)
    corp = models.ForeignKey(
        to='crm.Corp',
        verbose_name='Корпус',
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
    complex = models.ForeignKey(
        to='crm.Complex',
        verbose_name='ЖК',
        on_delete=models.CASCADE,
        related_name='old_buildings',
        null=True, blank=True,
    )

    class Meta:
        verbose_name: str = 'вторичка'
        verbose_name_plural: str = 'вторички'

    @property
    def type_building(self) -> str:
        return 'oldbuildinglot'

    @property
    def corp_name(self) -> str:
        if self.corp:
            return self.corp.name
        return ''


__all__ = (
    'Lot',
    'Plan',
    'NewBuildingLot',
    'OldBuildingLot',
)
