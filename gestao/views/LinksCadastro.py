from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from gestao import models
from gestao import forms

from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin, GestaoPermissoesMixin


class LinkCadastroListView(ListView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'links_cadastro/index.html'
    model = models.LinkCadastro
    paginate_by = 5
    ordering = ('usado', '-validade', '-data',)

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        queryset = models.LinkCadastro.objects.filter(
            Q(id__startswith=termo_pesquisa)
        )

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


class CriarLinkCadastroView(CreateView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'links_cadastro/novo.html'
    model = models.LinkCadastro
    form_class = forms.LinkCadastroForm
    success_url = reverse_lazy('gestao-links-cadastro')
    permission_required = 'gestao.add_linkcadastro'


class EditarLinkCadastroView(UpdateView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'links_cadastro/editar.html'
    model = models.LinkCadastro
    form_class = forms.LinkCadastroForm
    success_url = reverse_lazy('gestao-links-cadastro')
    permission_required = 'gestao.change_linkcadastro'


class RemoverLinkCadastroView(DeleteView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    model = models.LinkCadastro
    success_url = reverse_lazy('gestao-links-cadastro')
    permission_required = 'gestao.delete_linkcadastro'

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return self.post(request, *args, **kwargs)


class VerLinkCadastroView(DetailView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'links_cadastro/ver.html'
    model = models.LinkCadastro
    permission_required = 'gestao.view_linkcadastro'
