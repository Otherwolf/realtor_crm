from typing import Tuple

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.html import mark_safe

from crm.utils.base import images_upload_path

User = get_user_model()


class Complex(models.Model):
    updated_at = models.DateTimeField(auto_now=True, null=False, verbose_name='Дата изменения')
    name = models.CharField(verbose_name='Название', blank=True, null=False, max_length=128, default='')
    region = models.ForeignKey('crm.Region', verbose_name='Регион', null=True, on_delete=models.SET_NULL)
    address = models.TextField(max_length=256, verbose_name='Адрес', null=False, blank=False, default='')
    description = models.TextField(verbose_name='Описание', blank=True, default='', null=False, max_length=2048)
    end_of_construction = models.CharField(blank=True, null=False, default='', verbose_name='Сдача', max_length=256)
    count_lots = models.IntegerField(verbose_name='Количество лотов', blank=True, null=True)
    count_floors = models.IntegerField(verbose_name='Этажность', blank=True, null=True)

    # детали
    trim = models.CharField(verbose_name='Отделка', blank=True, null=False, max_length=256)
    facade = models.CharField(verbose_name='Фасад', blank=True, null=False, max_length=128, default='')
    elevators = models.CharField(verbose_name='Лифты', blank=True, null=False, max_length=128, default='')
    windows = models.CharField(verbose_name='Окна', blank=True, null=False, max_length=128, default='')
    ventilation = models.CharField(verbose_name='Вентиляция', blank=True, null=False, max_length=128, default='')
    conditioning = models.CharField(
        verbose_name='Кондиционирование',
        max_length=128,
        default='',
        blank=True, null=False,
    )
    # Юр. Детали
    cadastre = models.CharField(verbose_name='Кадастр', blank=True, null=False, max_length=128, default='')
    tax = models.CharField(verbose_name='Налог', blank=True, null=False, max_length=64, default='')
    content = models.TextField(verbose_name='Содержание', blank=True, null=False, max_length=512, default='')
    contract = models.CharField(verbose_name='Договор', blank=True, null=False, max_length=128, default='')
    ceilings = models.CharField(verbose_name='Потолки', blank=True, null=False, max_length=128, default='')
    parking = models.CharField(verbose_name='Паркинг', blank=True, null=False, max_length=128, default='')
    parking_price = models.CharField(verbose_name='Паркинг, р', blank=True, null=False, max_length=64, default='')
    mortgage = models.CharField(verbose_name='Ипотека', blank=True, null=False, max_length=128, default='')
    installment = models.CharField(verbose_name='Рассрочка', blank=True, null=False, max_length=128, default='')
    promotions = models.CharField(verbose_name='Акции', blank=True, null=False, max_length=256, default='')
    complex_infrastructure = models.CharField(
        verbose_name='Инфраструктура комплекса',
        max_length=256,
        default='',
        blank=True, null=False,
    )
    commercial_space = models.CharField(
        verbose_name='Коммерческие площади',
        max_length=128,
        default='',
        blank=True, null=False,
    )
    trade_registration = models.CharField(
        verbose_name='Регистрация сделки',
        max_length=128,
        default='',
        blank=True, null=False,
    )

    # Закрытые для клиента данные
    weekdays_from = models.IntegerField(null=False, blank=True, verbose_name='Будни с', default=9)
    weekdays_to = models.IntegerField(null=False, blank=True, verbose_name='Будни по', default=18)
    weekend_form = models.IntegerField(null=False, blank=True, verbose_name='Выходные с', default=9)
    weekend_to = models.IntegerField(null=False, blank=True, verbose_name='Выходные по', default=18)
    note = models.TextField(null=False, default='', blank=True, verbose_name='Примечание', max_length=516)
    parking_close = models.TextField(null=False, default='', blank=True, verbose_name='Паркинг', max_length=256)
    reward = models.CharField(null=True, verbose_name='Вознаграждение', blank=True, max_length=256)
    sales_office_address = models.TextField(
        default='',
        verbose_name='Адрес офиса продаж',
        max_length=256,
        null=False, blank=True,
    )

    updated_by = models.ForeignKey(
        to=User,
        verbose_name='Кем изменена',
        on_delete=models.SET_NULL,
        null=True,
    )
    developer = models.ForeignKey(
        to='crm.Developer',
        verbose_name='Застройщик',
        on_delete=models.CASCADE,
        related_name='complexes',
        null=True, blank=True,
    )
    near_metro = models.CharField(
        verbose_name='Ближайшее метро',
        max_length=256,
        default='',
        blank=True, null=True,
    )
    start_of_construction = models.CharField(
        default='',
        max_length=16,
        verbose_name='Начало строительства',
        blank=True, null=False,
    )
    construction_tech = models.ForeignKey(
        to='crm.ConstructionTech',
        verbose_name='Технология строительства',
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    premises_type = models.ForeignKey(
        to='crm.PremisesType',
        verbose_name='Тип помещения',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    object_class = models.ForeignKey(
        to='crm.ObjectClass',
        verbose_name='Класс объекта',
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    infrastructure = models.TextField(
        verbose_name='Инфраструктура',
        default='',
        max_length=2048,
        blank=True, null=False,
    )
    transport_accessibility = models.TextField(
        verbose_name='Транспортная доступность',
        default='',
        max_length=2048,
        blank=True, null=False,
    )

    class Meta:
        verbose_name: str = 'ЖК'
        verbose_name_plural: str = 'ЖК'
        ordering: Tuple[str, ...] = ('name',)

    def __str__(self) -> str:
        return self.name

    @property
    def count_lots_in_sale(self) -> int:
        return self.old_buildings.all().count() + self.new_buildings.all().count()

    @property
    def s_range(self) -> str:
        from django.db.models import Max, Min
        arr = set(self.old_buildings.aggregate(Max('s'), Min('s')).values())
        arr.update(self.new_buildings.aggregate(Max('s'), Min('s')).values())
        arr.discard(None)
        if len(arr):
            return '{0} - {1}'.format(min(arr), max(arr))
        return ''

    @property
    def min_price(self):
        from django.db.models import Min
        try:
            arr = set(self.old_buildings.filter(type_object__name__icontains='вартир') \
                      .aggregate(
                min_price_m=Min(models.F('price') / models.F('s'), output_field=models.IntegerField())).values())
            arr.update(list(self.new_buildings.filter(type_object__name__icontains='вартир') \
                            .aggregate(
                min_price_m=Min(models.F('price') / models.F('s'), output_field=models.IntegerField())).values()))
            arr.discard(None)
        except:
            return ''
        if len(arr):
            return '{0}'.format(min(arr))
        return ''

    @property
    def min_price_apart(self):
        from django.db.models import Min
        try:
            arr = set(self.old_buildings.filter(type_object__name__icontains='партамент') \
                      .aggregate(
                min_price_m=Min(models.F('price') / models.F('s'), output_field=models.IntegerField())).values())
            arr.update(list(self.new_buildings.filter(type_object__name__icontains='партамент') \
                            .aggregate(
                min_price_m=Min(models.F('price') / models.F('s'), output_field=models.IntegerField())).values()))
            arr.discard(None)
        except:
            return ''
        if len(arr):
            return '{0}'.format(min(arr))
        return ''


class Corp(models.Model):
    updated_at = models.DateTimeField(auto_now=True, null=False, verbose_name='Дата изменения')
    name = models.CharField(verbose_name='Название', blank=True, null=False, max_length=128, default='')
    count_lots = models.IntegerField(verbose_name='Количество лотов', blank=False, null=True)
    count_floors = models.IntegerField(verbose_name='Этажность', blank=True, null=True)
    end_of_construction = models.CharField(blank=True, default='', max_length=20, null=False, verbose_name='Сдача')
    complex = models.ForeignKey(
        to='crm.Complex',
        verbose_name='ЖК',
        related_name='floors',
        on_delete=models.CASCADE,
        blank=False, null=False,
    )
    updated_by = models.ForeignKey(
        to=User,
        verbose_name='Кем изменена',
        on_delete=models.DO_NOTHING,
        blank=False, null=False,
    )
    start_of_construction = models.CharField(
        blank=True, null=False,
        default='',
        max_length=20,
        verbose_name='Начало строительства',
    )
    premises_type = models.ForeignKey(
        to='crm.PremisesType',
        verbose_name='Тип помещения',
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name: str = 'Корпус'
        verbose_name_plural: str = 'Корпуса'

    def __str__(self) -> str:
        return self.name or self.complex


class Floor(models.Model):
    updated_at = models.DateTimeField(auto_now=True, null=False, verbose_name='Дата изменения')
    name = models.CharField(verbose_name='Название', blank=True, null=False, max_length=128, default='')
    plan = models.ImageField(upload_to=images_upload_path, blank=True, null=True, verbose_name='Планировка')
    updated_by = models.ForeignKey(
        to=User,
        verbose_name='Кем изменена',
        on_delete=models.DO_NOTHING,
        blank=False, null=False,
    )

    class Meta:
        verbose_name: str = 'План этажа'
        verbose_name_plural: str = 'Планы этажей'

    def __str__(self) -> str:
        return self.name or f'Планировка этажа №{self.id}'

    def image_tag(self) -> str:
        if self.plan:
            return mark_safe(f'<img src="/media/{self.plan}" width="350" height="auto" />')
        return 'Изображение отсутствует'

    image_tag.short_description = 'Image'


class Layout(models.Model):
    floor_from = models.IntegerField(verbose_name='Этаж с', null=False, blank=False, default=0)
    floor_to = models.IntegerField(verbose_name='Этаж по', null=False, blank=False, default=0)
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
        null=True, blank=True,
    )
    floor = models.ForeignKey(
        to='crm.Floor',
        verbose_name='Планировка эатажа',
        on_delete=models.CASCADE,
        null=False, blank=False,
    )

    class Meta:
        verbose_name: str = 'План этажа'
        verbose_name_plural: str = 'Планы этажей'

    def __str__(self) -> str:
        return f'Планировка в {self.corp}'


__all__ = (
    'Complex',
    'Corp',
    'Floor',
    'Layout',
)
