from django.contrib.admin import TabularInline
from django.utils.safestring import mark_safe

from crm import models


class ContactsInlineAdmin(TabularInline):
    extra = 0
    model = models.Contacts
    fields = ['name', 'email', 'phone', 'note']


class LinkInlineAdmin(TabularInline):
    extra = 0
    model = models.Link
    fields = ['name', 'link']


class LayoutInlineAdmin(TabularInline):
    extra = 0
    model = models.Layout
    fields = ['floor', 'floor_from', 'floor_to']


class DocumentInlineAdmin(TabularInline):
    extra = 0
    model = models.Document
    readonly_fields = ['get_created_at', 'get_size']
    fields = ['type', 'file', 'get_created_at', 'get_size']


class ImageInlineAdmin(TabularInline):
    extra = 0
    model = models.Image
    readonly_fields = ['get_created_at', 'get_size', 'image_preview']
    fields = ['image', 'get_created_at', 'get_size', 'image_preview']

    @staticmethod
    def image_preview(instance) -> str:
        """Preview"""
        # ex. the name of column is "image"
        if instance.image:
            return mark_safe(f'<img src="{instance.image.url}" width="250" height="auto" style="object-fit:contain" />')
        else:
            return '(No image)'


class TagInlineAdmin(TabularInline):
    extra = 0
    model = models.Tag
    fields = ['name']


__all__ = (
    'ContactsInlineAdmin',
    'LinkInlineAdmin',
    'LayoutInlineAdmin',
    'DocumentInlineAdmin',
    'ImageInlineAdmin',
    'TagInlineAdmin',
)
