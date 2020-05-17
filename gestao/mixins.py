from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.urls import resolve
from django.conf import settings
from django.shortcuts import render

from gestao.utilidades import areas

class GestaoContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['areas'] = areas
        context['area_ferramentas'] = areas[0].ferramentas
        context['nome_url'] = resolve(self.request.path_info).url_name
        context['grupos_padrao'] = settings.GESTAO_DEFAULT_GROUP_LIST
        context['termo'] = self.request.GET.get('termo', '')
        return context

class GestaoPermissoesMixin(PermissionRequiredMixin):
    def handle_no_permission(self):
        self.object = None
        return render(self.request, 'erros/403.html', self.get_context_data())


class GestaoRegrasMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/gestao/login'

    def test_func(self):
        if self.request.user.groups.filter(pk=1).exists() or self.request.user.is_superuser:
            return True

        return False
