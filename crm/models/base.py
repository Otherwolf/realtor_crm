import datetime
import os
from typing import Tuple

from django.db import models

from crm.consts import (DOCUMENT_TYPES)
from crm.utils.base import documents_upload_path, images_upload_path


class Region(models.Model):
    name = models.CharField(verbose_name='Название региона', blank=False, null=False, max_length=128)

    class Meta:
        verbose_name: str = 'регион'
        verbose_name_plural: str = 'регионы'
        ordering: Tuple[str, ...] = ('name',)

    def __str__(self) -> str:
        return self.name


class ConstructionTech(models.Model):
    name = models.CharField(verbose_name='Технология строительства', blank=False, null=False, max_length=128)

    class Meta:
        verbose_name: str = 'технология строительства'
        verbose_name_plural: str = 'технологии строительства'
        ordering: Tuple[str, ...] = ('name',)

    def __str__(self) -> str:
        return self.name


class PremisesType(models.Model):
    name = models.CharField(verbose_name='Тип помещения', blank=False, null=False, max_length=128)

    class Meta:
        verbose_name: str = 'Тип помещения'
        verbose_name_plural: str = 'Типы помещения'
        ordering: Tuple[str, ...] = ('name',)

    def __str__(self) -> str:
        return self.name


class ObjectClass(models.Model):
    name = models.CharField(verbose_name='Класс объекта', blank=False, null=False, max_length=128)

    class Meta:
        verbose_name: str = 'Класс объекта'
        verbose_name_plural: str = 'Классы объектов'
        ordering: Tuple[str, ...] = ('name',)

    def __str__(self) -> str:
        return self.name


class Contacts(models.Model):
    name = models.CharField(verbose_name='Контактное лицо', blank=True, null=False, max_length=128, default='')
    phone = models.CharField(verbose_name='Телефон', blank=True, null=False, max_length=128, default='')
    email = models.EmailField(verbose_name='E-mail', blank=True, null=False, max_length=64, default='')
    note = models.CharField(verbose_name='Примечание', blank=True, null=False, max_length=256, default='')
    developer = models.ForeignKey(
        to='crm.Developer',
        verbose_name='Застройщик',
        related_name='contacts',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    complex = models.ForeignKey(
        to='crm.Complex',
        verbose_name='ЖК',
        related_name='contacts',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    lot = models.ForeignKey(
        to='crm.Lot',
        verbose_name='Лот',
        related_name='contacts',
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name: str = 'контакт'
        verbose_name_plural: str = 'контакты'
        ordering: Tuple[str, ...] = ('name',)

    def __str__(self) -> str:
        return self.name


class Link(models.Model):
    name = models.CharField(verbose_name='Название', blank=True, null=False, max_length=30, default='')
    link = models.CharField(verbose_name='Ссылка', max_length=128, null=False, blank=True, default='')
    complex = models.ForeignKey(
        to='crm.Complex',
        verbose_name='ЖК',
        related_name='links',
        on_delete=models.CASCADE,
        null=True,
    )
    lot = models.ForeignKey(
        to='crm.Lot',
        verbose_name='Лот',
        related_name='links',
        on_delete=models.CASCADE,
        null=True,
    )
    developer = models.ForeignKey(
        to='crm.Developer',
        verbose_name='застройщик',
        related_name='links',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name: str = 'Ссылка'
        verbose_name_plural: str = 'Ссылки'
        ordering: Tuple[str, ...] = ('name',)

    def __str__(self) -> str:
        return self.name


class Document(models.Model):
    file = models.FileField(upload_to=documents_upload_path, max_length=512, verbose_name='Файл')
    type = models.CharField(max_length=64, choices=DOCUMENT_TYPES, verbose_name='Тип документа')
    lot = models.ForeignKey('crm.Lot', verbose_name='Лот', related_name='files', null=True, on_delete=models.CASCADE)
    complex = models.ForeignKey(
        to='crm.Complex',
        verbose_name='ЖК',
        related_name='files',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name: str = 'Документ'
        verbose_name_plural: str = 'Документы'
        ordering: Tuple[str, ...] = ('type',)

    def __str__(self) -> str:
        return self.filename

    @property
    def get_size(self) -> str:
        """Размер"""
        if os.path.exists(self.file.path):
            return "%0.1f KB" % (os.path.getsize(self.file.path) / (1024.0))
        return "0 MB"

    @property
    def get_created_at(self):
        if self.file:
            statbuf = os.stat(self.file.path)
            return datetime.datetime.utcfromtimestamp(statbuf.st_ctime).date()
        return ''

    get_created_at.fget.short_description = u'Дата загрузки'

    @property
    def get_url(self):
        if self.file:
            return self.file.url
        return ''

    @property
    def filename(self):
        return os.path.basename(self.file.name)


class Image(models.Model):
    image = models.ImageField(upload_to=images_upload_path, null=False, verbose_name='Изображение')
    complex = models.ForeignKey(
        to='crm.Complex',
        verbose_name='ЖК',
        related_name='images',
        on_delete=models.CASCADE,
        null=True,
    )
    lot = models.ForeignKey(
        to='crm.Lot',
        verbose_name='Лот',
        related_name='images',
        on_delete=models.CASCADE,
        null=True,
    )
    developer = models.ForeignKey(
        to='crm.Developer',
        related_name='images',
        verbose_name='Застройщик',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name: str = 'Изображение'
        verbose_name_plural: str = 'Изображения'

    def __str__(self) -> str:
        return 'image_' + str(self.id)

    @property
    def get_size(self):
        if os.path.exists(self.image.path):
            return "%0.1f KB" % (os.path.getsize(self.image.path) / (1024.0))
        return "0 MB"

    get_size.fget.short_description = u'Размер'

    @property
    def get_created_at(self):
        if os.path.exists(self.image.path):
            statbuf = os.stat(self.image.path)
            return datetime.datetime.utcfromtimestamp(statbuf.st_ctime).date()
        return ''

    get_created_at.fget.short_description = u'Дата загрузки'

    @property
    def get_url(self):
        if self.image:
            return self.image.url
        else:
            return ''


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        unique=True,
        default='',
        max_length=128,
        null=False, blank=False,
    )
    complex = models.ForeignKey(
        to='crm.Complex',
        verbose_name='ЖК',
        related_name='tags',
        on_delete=models.CASCADE,
        null=True,
    )
    lot = models.ForeignKey(
        to='crm.Lot',
        verbose_name='Лот',
        related_name='tags',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name: str = 'Тег'
        verbose_name_plural: str = 'Теги'

    def __str__(self) -> str:
        return self.name


__all__ = (
    'Region',
    'ConstructionTech',
    'PremisesType',
    'ObjectClass',
    'Contacts',
    'Link',
    'Document',
    'Image',
    'Tag',
)
