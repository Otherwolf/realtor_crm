from django.views.generic import TemplateView


class BaseView(TemplateView):
    template_name: str = 'base/index.html'


__all__ = ('BaseView',)
