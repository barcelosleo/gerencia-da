from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from gestao import models
from gestao import forms

from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin

class AssociadoListView(ListView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'associados/index.html'
    model = models.Associado
    paginate_by = 5

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        context = models.Associado.objects.filter(
            Q(is_active=True) &
            (
                Q(nome__startswith=termo_pesquisa) |
                Q(sobrenome__startswith=termo_pesquisa) |
                Q(email__startswith=termo_pesquisa) |
                Q(telefone__startswith=termo_pesquisa) |
                Q(matricula__startswith=termo_pesquisa)
            )
        )
        return context

class CriarAssociadoView(CreateView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'associados/novo.html'
    model = models.Associado
    form_class = forms.AssociadoForm
    success_url = reverse_lazy('gestao-associados')

class EditarAssociadoView(UpdateView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'associados/editar.html'
    model = models.Associado
    form_class = forms.AssociadoForm
    success_url = reverse_lazy('gestao-associados')

class RemoverAssociadoView(DeleteView, GestaoRegrasMixin):
    model = models.Associado
    success_url = reverse_lazy('gestao-associados')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class VerAssociadoView(DetailView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'associados/ver.html'
    model = models.Associado
