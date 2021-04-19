from itertools import chain

from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from crm.models.complexes import Complex
from crm.models.developers import Developer
from crm.models.lots import (OldBuildingLot, NewBuildingLot)
from crm.serializers import (
    ProfileSerializer, ComplexesShortSerializer, OldBuildingsShortSerializer,
    NewBuildingsShortSerializer, MainDeveloperSerializer, MainComplexSerializer,
    MainOldSerializer, DeveloperSubSerializer
)


class ProfileRest(APIView):
    ser = ProfileSerializer

    def get(self, request, *args, **kwargs):
        ser_data = self.ser(request.user)
        return Response(ser_data.data)


class LoadDataRest(APIView):
    ser = OldBuildingsShortSerializer
    ser1 = NewBuildingsShortSerializer
    ser2 = ComplexesShortSerializer
    ser3 = DeveloperSubSerializer

    @staticmethod
    def is_empty(value) -> bool:
        return value is None or value == '' or value == []

    def filter_by(self, querySet, property, value):
        if hasattr(querySet.model, property.split('__')[0]) and not self.is_empty(value):
            return querySet.exclude(**{property: value})
        return querySet

    def post(self, request, *args, **kwargs):
        page = request.data.get('page')
        counter = request.data.get('counter')
        filter = request.data.get('filter')

        if page == 'developers':
            objs = Developer.objects.all().order_by('name')
        if page == 'complexes':
            objs = Complex.objects.all().order_by('developer')
        if page == 'lots':
            new_buildings = NewBuildingLot.objects.all().order_by('complex')
            old_buildings = OldBuildingLot.objects.all().order_by('complex')
            price_for = filter.get('priceFor')
            for key, value in filter.items():
                if self.is_empty(value):
                    continue
                if key == 'selectedType':
                    if value == 'new':
                        old_buildings = old_buildings.exclude(id__gt=0)
                    if value == 'old':
                        new_buildings = new_buildings.exclude(id__gt=0)
                if key == 'bedroom':
                    new_buildings = new_buildings.filter(name__in=value)
                    old_buildings = old_buildings.filter(name__in=value)
                if price_for == 'м²' and (key == 'price__gt' or key == 'price__lt'):
                    key = 'price_m__{0}'.format(key.split('__')[1])
                    new_buildings = new_buildings.annotate(price_m=F('price') / F('s')).exclude(**{key: int(value)})
                    old_buildings = old_buildings.annotate(price_m=F('price') / F('s')).exclude(**{key: int(value)})
                new_buildings = self.filter_by(new_buildings, key, value)
                old_buildings = self.filter_by(old_buildings, key, value)
            objs = list(
                sorted(
                    chain(new_buildings, old_buildings),
                    key=lambda objects: objects.id
                ))

        paginator = Paginator(objs, 30)
        try:
            data_page = paginator.page(counter)
        except Exception:
            return Response([])
        if page == 'complexes':
            ser_data = self.ser2(data_page, many=True)
        if page == 'lots':
            ser_data = self.ser1(data_page, many=True)
        if page == 'developers':
            ser_data = self.ser3(data_page, many=True)
        return Response(ser_data.data)


class LoadMainRest(APIView):
    ser_dev = MainDeveloperSerializer
    ser_com = MainComplexSerializer
    ser_old = MainOldSerializer

    def post(self, request, *args, **kwargs):
        id = request.data.get('id')
        type = request.data.get('type')
        if type == 'developer':
            obj = get_object_or_404(Developer, id=id)
            ser_data = self.ser_dev(obj)
        if type == 'complex':
            obj = get_object_or_404(Complex, id=id)
            ser_data = self.ser_com(obj)
        if type == 'newbuildinglot':
            obj = get_object_or_404(NewBuildingLot, id=id)
            ser_data = self.ser_new(obj)
        if type == 'oldbuildinglot':
            obj = get_object_or_404(OldBuildingLot, id=id)
            ser_data = self.ser_old(obj)
        return Response(ser_data.data)


__all__ = ('ProfileRest', 'LoadDataRest', 'LoadMainRest',)
