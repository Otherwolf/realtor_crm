from typing import List

from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (path, URLPattern)

from project import settings

urlpatterns: List[URLPattern] = [
    path(route='grappelli/', view=include(arg='grappelli.urls', namespace='grappelli')),
    path(route='admin/', view=admin.site.urls),
    path(route='', view=include(arg='crm.urls', namespace='crm')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

__all__ = ('urlpatterns',)
