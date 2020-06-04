from django.views.generic.base import ContextMixin
from django.urls import resolve

from gestao.utilidades import areas
from gestao.mixins import GestaoRegrasMixin, GestaoPermissoesMixin

class FinanceiroContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['areas'] = areas
        context['area_ferramentas'] = areas[1].ferramentas
        context['nome_url'] = resolve(self.request.path_info).url_name
        context['termo'] = self.request.GET.get('termo', '')
        return context

class FinanceiroMixin(GestaoRegrasMixin, FinanceiroContextMixin):
    pass

class FinanceiroProtegidoMixin(GestaoRegrasMixin, GestaoPermissoesMixin, FinanceiroContextMixin):
    pass
