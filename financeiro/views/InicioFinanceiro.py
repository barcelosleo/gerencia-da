from django.urls import reverse_lazy

from django.views.generic.detail import DetailView

from gestao.mixins import GestaoRegrasMixin
from financeiro.mixins import FinanceiroContextMixin

from gestao import models as gestao

class InicioFinanceiroView(DetailView, GestaoRegrasMixin, FinanceiroContextMixin):
    template_name = 'gestor/index.html'
    model = gestao.Diretor

    def get_object(self):
        return self.request.user