from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from gestao import models
from gestao import forms

from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin, GestaoPermissoesMixin

class ReuniaoListView(ListView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'atas/index.html'
    model = models.Reuniao
    paginate_by = 5
    ordering = ('id',)

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')

        queryset = models.Reuniao.objects.filter(
            Q(data__startswith=termo_pesquisa) | Q(titulo__startswith=termo_pesquisa)
        )

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

class CriarReuniaoView(CreateView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'atas/nova.html'
    model = models.Reuniao
    form_class = forms.ReuniaoForm
    success_url = reverse_lazy('gestao-reunioes')
    permission_required = 'gestao.add_reuniao'

class EditarReuniaoView(UpdateView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'atas/editar.html'
    model = models.Reuniao
    form_class = forms.ReuniaoForm
    success_url = reverse_lazy('gestao-reunioes')
    permission_required = 'gestao.change_reuniao'

class RemoverReuniaoView(DeleteView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    model = models.Reuniao
    success_url = reverse_lazy('gestao-reunioes')
    permission_required = 'gestao.delete_reuniao'

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return self.post(request, *args, **kwargs)

class VerReuniaoView(DetailView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'atas/ver.html'
    model = models.Reuniao
    permission_required = 'gestao.view_reuniao'