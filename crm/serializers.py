from typing import Tuple

from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from crm.models import (
    Developer,
    Complex,
    NewBuildingLot,
    OldBuildingLot,
    Image,
    Contacts,
    Region,
    ObjectClass,
    PremisesType,
    ConstructionTech,
    Link,
    Document,
    Corp
)


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields: Tuple[str, ...] = ('id', 'get_url')


class ShortCorpSerializer(ModelSerializer):
    class Meta:
        model = Corp
        fields: Tuple[str, ...] = ('id', 'name')


class LinkSerializer(ModelSerializer):
    class Meta:
        model = Link
        fields: Tuple[str, ...] = ('name', 'link')


class FileSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields: Tuple[str, ...] = ('type', 'get_size', 'get_created_at', 'get_url', 'filename')


class ClassObjectSerializer(ModelSerializer):
    class Meta:
        model = ObjectClass
        fields: Tuple[str, ...] = ('name',)


class ConstructionTechSerializer(ModelSerializer):
    class Meta:
        model = ConstructionTech
        fields: Tuple[str, ...] = ('name',)


class PremisesTypeSerializer(ModelSerializer):
    class Meta:
        model = PremisesType
        fields: Tuple[str, ...] = ('name',)


class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields: Tuple[str, ...] = ('name',)


class ContactsSerializer(ModelSerializer):
    class Meta:
        model = Contacts
        fields: Tuple[str, ...] = ('id', 'name', 'phone', 'email', 'note',)


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields: Tuple[str, ...] = ('id', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff')


class DeveloperSubSerializer(ModelSerializer):
    class Meta:
        model = Developer
        fields: Tuple[str, ...] = ('id', 'name', 'count_complexes')


class ComplexSubSerializer(ModelSerializer):
    class Meta:
        model = Complex
        fields: Tuple[str, ...] = ('id', 'name', 'count_lots_in_sale')


class ComplexesShortSerializer(ModelSerializer):
    developer = DeveloperSubSerializer()

    class Meta:
        model = Complex
        fields: Tuple[str, ...] = ('id', 'name', 'developer', 'end_of_construction', 'address', 'count_lots_in_sale')


class OldBuildingsShortSerializer(ModelSerializer):
    complex = ComplexSubSerializer()
    corp = ShortCorpSerializer()

    class Meta:
        model = OldBuildingLot
        fields: Tuple[str, ...] = (
            'id', '__str__', 'status', 'floor',
            'corp', 's', 'type_building', 'price',
            'complex', 'url_plan', 'n_on_price', 'floor',
            'price_per_m', 'corp_name'
        )


class NewBuildingsShortSerializer(ModelSerializer):
    complex = ComplexSubSerializer()
    corp = ShortCorpSerializer()

    class Meta:
        model = NewBuildingLot
        fields: Tuple[str, ...] = (
            'id', 'price_per_m', 'type_building', 'corp_name',
            'floor', '__str__', 'n_on_price', 'status',
            's', 'corp', 'price', 'complex', 'url_plan'
        )


class MainDeveloperSerializer(ModelSerializer):
    updated_by = ProfileSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    description = serializers.SerializerMethodField()
    contacts = ContactsSerializer(many=True, read_only=True)
    complexes = ComplexesShortSerializer(many=True, read_only=True)
    links = LinkSerializer(many=True, read_only=True)

    @staticmethod
    def get_description(instance):
        return mark_safe(instance.description)

    class Meta:
        model = Developer
        fields: Tuple[str, ...] = (
            'id', 'contacts', 'links', 'updated_by',
            'updated_at', 'name', 'created_at', 'description',
            'objects_delivered', 'objects_under_construction',
            'images', 'complexes'
        )


class MainComplexSerializer(ModelSerializer):
    updated_by = ProfileSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    contacts = ContactsSerializer(many=True, read_only=True)
    region = RegionSerializer()
    developer = DeveloperSubSerializer()
    object_class = ClassObjectSerializer()
    premises_type = PremisesTypeSerializer()
    construction_tech = ConstructionTechSerializer()
    links = LinkSerializer(many=True, read_only=True)
    files = FileSerializer(many=True)

    class Meta:
        model = Complex
        fields: Tuple[str, ...] = (
            'id', 'reward', 'updated_by', 'updated_at',
            'images', 'name', 'contacts', 'links',
            'region', 'address', 'description', 'developer',
            'end_of_construction', 'start_of_construction', 'object_class',
            'near_metro', 'count_lots', 'premises_type',
            'count_floors', 'count_lots_in_sale', 's_range',
            'min_price', 'min_price_apart', 'infrastructure',
            'transport_accessibility', 'construction_tech', 'trim',
            'facade', 'elevators', 'windows', 'ventilation',
            'conditioning', 'cadastre', 'tax',
            'files', 'content', 'contract',
            'ceilings', 'parking', 'parking_price',
            'trade_registration', 'mortgage', 'installment',
            'promotions', 'complex_infrastructure', 'commercial_space',
            'weekdays_from', 'weekdays_to', 'weekend_form',
            'weekend_to', 'sales_office_address', 'note',
            'parking_close'
        )


class MainOldSerializer(ModelSerializer):
    updated_by = ProfileSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    contacts = ContactsSerializer(many=True, read_only=True)
    links = LinkSerializer(many=True, read_only=True)
    files = FileSerializer(many=True)
    complex = MainComplexSerializer(read_only=True)
    type_object = PremisesTypeSerializer(read_only=True)
    corp = ShortCorpSerializer(read_only=True)

    class Meta:
        model = OldBuildingLot
        fields: Tuple[str, ...] = (
            'id', 'complex', 'corp', 'updated_by',
            'updated_at', '__str__', 'files', 'contacts',
            'links', 'lease', 'url_plan', 'images', 'n_on_price',
            'type_object', 'floor', 's', 'trim',
            'view_from_windows', 'options', 'reward',
            'price', 'currency', 'price_per_m', 'currency_per_m'
        )


__all__ = (
    'ImageSerializer',
    'ShortCorpSerializer',
    'LinkSerializer',
    'FileSerializer',
    'ClassObjectSerializer',
    'ConstructionTechSerializer',
    'PremisesTypeSerializer',
    'RegionSerializer',
    'ContactsSerializer',
    'ProfileSerializer',
    'DeveloperSubSerializer',
    'ComplexSubSerializer',
    'ComplexesShortSerializer',
    'OldBuildingsShortSerializer',
    'NewBuildingsShortSerializer',
    'MainDeveloperSerializer',
    'MainComplexSerializer',
    'MainOldSerializer',
)
