from django.contrib.admin import (ModelAdmin, register)
from django.contrib.admin.models import LogEntry

from crm.admin.inline import *
from crm.models import *


@register(users.UserProfile)
class ProfileAdmin(ModelAdmin):
    fields = ['user', 'phone']
    list_display = ('id', '__str__', 'user', 'phone',)
    search_fields = [
        'user__last_name',
        'user__first_name',
        'phone',
        'user__email',
        'user__username'
    ]


@register(LogEntry)
class LogEntryAdmin(ModelAdmin):
    list_display = (
        'id',
        'content_type',
        'object_repr',
        'user',
        'is_addition',
        'is_change',
        'is_deletion',
    )
    readonly_fields = (
        'action_time',
        'user',
        'content_type',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message',
    )

    list_filter = [
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        return []

    def is_addition(self, obj):
        return obj.is_addition()

    is_addition.short_description = 'Добавление'
    is_addition.boolean = True

    def is_change(self, obj):
        return obj.is_change()

    is_change.short_description = 'Изменение'
    is_change.boolean = True

    def is_deletion(self, obj):
        return obj.is_deletion()

    is_deletion.short_description = 'Удаление'
    is_deletion.boolean = True


@register(developers.Developer)
class DeveloperAdmin(ModelAdmin):
    list_display = ('id', '__str__', 'updated_by', 'updated_at',)
    readonly_fields = ['updated_by', 'updated_at']
    search_fields = ['name', ]
    inlines = (
        ContactsInlineAdmin,
        ImageInlineAdmin,
        LinkInlineAdmin
    )

    def get_fieldsets(self, request, obj=None):
        full_fieldsets = [
            ('Сведения о застройщике', {'fields': (
                'name',
                'created_at',
                'description',
                'objects_delivered',
                'objects_under_construction'
            )}),
            ('Административная информация', {'fields': (
                'updated_at',
                'updated_by'
            )})
        ]
        self.fieldsets = full_fieldsets
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)


@register(base.Region)
class RegionAdmin(ModelAdmin):
    fields = ['name']
    list_display = ['name']
    search_fields = ['name', ]


@register(base.ConstructionTech)
class ConstructionTechAdmin(ModelAdmin):
    fields = ['name']
    search_fields = ['name', ]


@register(base.PremisesType)
class PremisesTypeAdmin(ModelAdmin):
    fields = ['name']
    search_fields = ['name', ]


@register(base.ObjectClass)
class ObjectClassAdmin(ModelAdmin):
    fields = ['name']
    search_fields = ['name', ]


@register(complexes.Complex)
class ComplexAdmin(ModelAdmin):
    list_display = ('id', '__str__', 'updated_by', 'updated_at',)
    readonly_fields = ['updated_by', 'updated_at']
    search_fields = ['__all__', ]
    inlines = (
        LayoutInlineAdmin,
        LinkInlineAdmin,
        ImageInlineAdmin,
        DocumentInlineAdmin,
        ContactsInlineAdmin,
        TagInlineAdmin
    )

    def get_fieldsets(self, request, obj=None):
        full_fieldsets = [
            ('Сведения о ЖК', {'fields': (
                'name',
                'region',
                'address',
                'developer',
                'near_metro',
                'description',
                'start_of_construction',
                'end_of_construction',
                'construction_tech',
                'premises_type',
                'object_class',
                'count_lots',
                'count_floors',
                'infrastructure',
                'transport_accessibility',
                'reward'
            )}),
            ('Детали', {'fields': (
                'trim',
                'facade',
                'elevators',
                'windows',
                'ventilation',
                'conditioning'
            )}),
            ('Юридические детали', {'fields': (
                'cadastre',
                'tax',
                'content',
                'contract',
                'ceilings',
                'parking',
                'parking_price',
                'trade_registration',
                'mortgage',
                'installment',
                'promotions',
                'complex_infrastructure',
                'commercial_space'
            )}),
            ('Закрытые для клиента данные', {'fields': (
                'weekdays_from',
                'weekdays_to',
                'weekend_form',
                'weekend_to',
                'sales_office_address',
                'note',
                'parking_close'
            )}),
            ('Административная информация', {'fields': (
                'updated_at',
                'updated_by'
            )})
        ]
        self.fieldsets = full_fieldsets
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)


@register(complexes.Floor)
class FloorAdmin(ModelAdmin):
    list_display = ('id', '__str__', 'updated_by', 'updated_at', 'image_tag')
    readonly_fields = ['updated_by', 'updated_at', 'image_tag']
    search_fields = ['__all__', ]

    def get_fieldsets(self, request, obj=None):
        full_fieldsets = [
            ('Информация по этажу', {'fields': (
                'name',
                'plan',
                'image_tag'
            )}),
            ('Административная информация', {'fields': (
                'updated_at',
                'updated_by'
            )})
        ]
        self.fieldsets = full_fieldsets
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)


@register(complexes.Corp)
class CorpAdmin(ModelAdmin):
    list_display = ('id', '__str__', 'updated_by', 'updated_at',)
    search_fields = ['__all__', ]
    readonly_fields = ['updated_by', 'updated_at']
    inlines = (
        LayoutInlineAdmin,
    )

    def get_fieldsets(self, request, obj=None):
        full_fieldsets = [
            ('Информация по этажу', {'fields': (
                'name',
                'complex',
                'start_of_construction',
                'end_of_construction',
                'premises_type',
                'count_lots',
                'count_floors'
            )}),
            ('Административная информация', {'fields': (
                'updated_at',
                'updated_by'
            )})
        ]
        self.fieldsets = full_fieldsets
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)


class LotAdmin(ModelAdmin):
    list_display = ('id', '__str__', 'updated_by', 'updated_at',)
    search_fields = ['__all__', ]
    readonly_fields = ['updated_by', 'updated_at', ]
    inlines = (
        ImageInlineAdmin,
        LinkInlineAdmin,
        DocumentInlineAdmin,
        ContactsInlineAdmin,
        TagInlineAdmin
    )

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)


@register(lots.Plan)
class PlanAdmin(ModelAdmin):
    list_display = ('id', '__str__', 'updated_by', 'updated_at', 'image_tag')
    readonly_fields = ['updated_by', 'updated_at', 'image_tag']
    search_fields = ['__all__', ]

    def get_fieldsets(self, request, obj=None):
        full_fieldsets = [
            ('Информация по этажу', {'fields': (
                'name',
                'plan_floor',
                'plan',
                'image_tag'
            )}),
            ('Административная информация', {'fields': (
                'updated_at',
                'updated_by'
            )})
        ]
        self.fieldsets = full_fieldsets
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)


@register(lots.NewBuildingLot)
class NewBuildingLotAdmin(LotAdmin):
    def get_fieldsets(self, request, obj=None):
        full_fieldsets = [
            ('Общая информация', {'fields': (
                'status',
                'complex',
                'lease',
            )}),
            ('Информация по лоту', {'fields': (
                'name',
                'n_on_price',
                'type_object',
                'corp',
                'floor',
                's',
                'trim',
                'view_from_windows',
                'options',
                'reward',
                'currency',
                'price',
                'comment',
                'plan'
            )}),
            ('Административная информация', {'fields': (
                'updated_at',
                'updated_by'
            )})
        ]
        self.fieldsets = full_fieldsets
        return super().get_fieldsets(request, obj)


@register(lots.OldBuildingLot)
class OldBuildingLotAdmin(LotAdmin):
    def get_fieldsets(self, request, obj=None):
        full_fieldsets = [
            ('Общая информация', {'fields': (
                'status',
                'complex',
                'lease',
            )}),
            ('Информация по лоту', {'fields': (
                'name',
                'n_on_price',
                'type_object',
                'corp',
                'floor',
                's',
                'trim',
                'view_from_windows',
                'options',
                'reward',
                'currency',
                'price',
                'comment',
                'plan'
            )}),
            ('Административная информация', {'fields': (
                'updated_at',
                'updated_by'
            )})
        ]
        self.fieldsets = full_fieldsets
        return super().get_fieldsets(request, obj)


__all__ = (
    'ProfileAdmin',
    'LogEntryAdmin',
    'DeveloperAdmin',
    'RegionAdmin',
    'ConstructionTechAdmin',
    'PremisesTypeAdmin',
    'ObjectClassAdmin',
    'ComplexAdmin',
    'FloorAdmin',
    'CorpAdmin',
    'LotAdmin',
    'PlanAdmin',
    'NewBuildingLotAdmin',
    'OldBuildingLotAdmin',
)
