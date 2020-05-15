from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.contrib.auth.models import Group, Permission

from gestao import forms
from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin

class GrupoListView(ListView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'grupos/index.html'
    model = Group
    paginate_by = 5

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        context = Group.objects.filter(
            Q(name__startswith=termo_pesquisa)
        )
        return context

class CriarGrupoView(CreateView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'grupos/novo.html'
    model = Group
    form_class = forms.GrupoForm
    success_url = reverse_lazy('gestao-grupos')

class EditarGrupoView(UpdateView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'grupos/editar.html'
    model = Group
    form_class = forms.GrupoForm
    success_url = reverse_lazy('gestao-grupos')

class RemoverGrupoView(DeleteView, GestaoRegrasMixin):
    model = Group
    success_url = reverse_lazy('gestao-grupos')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class VerGrupoView(DetailView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'grupos/ver.html'
    model = Group

class GerenciarPermissoesView(ListView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'grupos/gerenciar_permissoes.html'
    model = Permission

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        context = Group.objects.get(pk=pk).permissions.all()
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['group'] = Group.objects.get(pk=pk)
        return context

