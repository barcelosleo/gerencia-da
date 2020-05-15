from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin
from django.urls import resolve

from gestao.utilidades import areas

class GestaoContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['areas'] = areas
        context['area_ferramentas'] = areas[0].ferramentas
        context['nome_url'] = resolve(self.request.path_info).url_name
        return context

class GestaoRegrasMixin(LoginRequiredMixin):
    login_url = '/gestao/login'