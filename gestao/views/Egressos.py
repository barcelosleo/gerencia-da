from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from gestao import models
from gestao import forms

from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin, GestaoPermissoesMixin

class EgressoListView(ListView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'egressos/index.html'
    model = models.Egresso
    paginate_by = 5
    ordering = ('id',)

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        queryset = models.Egresso.objects.filter(
            Q(nome__startswith=termo_pesquisa) |
            Q(sobrenome__startswith=termo_pesquisa) |
            Q(email__startswith=termo_pesquisa) |
            Q(telefone__startswith=termo_pesquisa) |
            Q(matricula__startswith=termo_pesquisa)
        )

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

class CriarEgressoView(CreateView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'egressos/novo.html'
    model = models.Egresso
    form_class = forms.EgressoForm
    success_url = reverse_lazy('gestao-egressos')
    permission_required = 'gestao.add_egresso'

    def form_valid(self, form):
        self.object = self.model.objects.create(**form.cleaned_data)
        return super().form_valid(form)

class EditarEgressoView(UpdateView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'egressos/editar.html'
    model = models.Egresso
    form_class = forms.EgressoForm
    success_url = reverse_lazy('gestao-egressos')
    permission_required = 'gestao.change_egresso'

class RemoverEgressoView(DeleteView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    model = models.Egresso
    success_url = reverse_lazy('gestao-egressos')
    permission_required = 'gestao.delete_egresso'

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return self.post(request, *args, **kwargs)

class VerEgressoView(DetailView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'egressos/ver.html'
    model = models.Egresso
    permission_required = 'gestao.view_egresso'
