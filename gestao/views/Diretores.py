from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from gestao import models
from gestao import forms

from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin, GestaoPermissoesMixin


class DiretorListView(ListView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'diretores/index.html'
    model = models.Diretor
    paginate_by = 5
    ordering = ('id',)

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        queryset = models.Diretor.objects.filter(
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


class CriarDiretorView(CreateView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'diretores/novo.html'
    model = models.Diretor
    form_class = forms.AssociadoForm
    success_url = reverse_lazy('gestao-diretores')
    permission_required = 'gestao.add_diretor'

    def form_valid(self, form):
        models.Diretor.objects.create(**form.cleaned_data)
        return redirect(self.success_url)


class EditarDiretorView(UpdateView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'diretores/editar.html'
    model = models.Diretor
    form_class = forms.AssociadoForm
    success_url = reverse_lazy('gestao-diretores')
    permission_required = 'gestao.change_diretor'


class RemoverDiretorView(DeleteView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    model = models.Diretor
    success_url = reverse_lazy('gestao-diretores')
    permission_required = 'gestao.delete_diretor'

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_staff = False
        self.object.save()

        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)


class VerDiretorView(DetailView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'diretores/ver.html'
    model = models.Diretor
    permission_required = 'gestao.view_diretor'
