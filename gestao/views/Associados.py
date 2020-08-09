from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from gestao import models
from gestao import forms

from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin, GestaoPermissoesMixin


class AssociadoListView(ListView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'associados/index.html'
    model = models.Associado
    paginate_by = 5
    ordering = ('id',)

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        queryset = models.Associado.objects.filter(
            Q(is_active=True) &
            (
                    Q(nome__startswith=termo_pesquisa) |
                    Q(sobrenome__startswith=termo_pesquisa) |
                    Q(email__startswith=termo_pesquisa) |
                    Q(telefone__startswith=termo_pesquisa) |
                    Q(matricula__startswith=termo_pesquisa)
            )
        )

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


class CriarAssociadoView(CreateView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'associados/novo.html'
    model = models.Aluno
    form_class = forms.AssociadoForm
    success_url = reverse_lazy('gestao-associados')
    permission_required = 'gestao.add_aluno'

    def form_valid(self, form):
        models.Aluno.objects.create(**form.cleaned_data)
        return redirect(self.success_url)


class EditarAssociadoView(UpdateView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'associados/editar.html'
    model = models.Aluno
    form_class = forms.AssociadoForm
    success_url = reverse_lazy('gestao-associados')
    permission_required = 'gestao.change_aluno'


class RemoverAssociadoView(DeleteView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    model = models.Associado
    success_url = reverse_lazy('gestao-associados')
    permission_required = 'gestao.delete_aluno'

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return self.post(request, *args, **kwargs)


class VerAssociadoView(DetailView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'associados/ver.html'
    model = models.Associado
    permission_required = 'gestao.view_aluno'
