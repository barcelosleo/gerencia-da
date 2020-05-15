from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from gestao import models
from gestao import forms

from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin

class EgressoListView(ListView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'egressos/index.html'
    model = models.Egresso
    paginate_by = 5

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        context = models.Egresso.objects.filter(
            Q(nome__startswith=termo_pesquisa) |
            Q(sobrenome__startswith=termo_pesquisa) |
            Q(email__startswith=termo_pesquisa) |
            Q(telefone__startswith=termo_pesquisa) |
            Q(matricula__startswith=termo_pesquisa)
        )
        return context

class CriarEgressoView(CreateView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'egressos/novo.html'
    model = models.Egresso
    form_class = forms.EgressoForm
    success_url = reverse_lazy('gestao-egressos')

    def form_valid(self, form):
        self.object = self.model.objects.create(**form.cleaned_data)
        return super().form_valid(form)

class EditarEgressoView(UpdateView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'egressos/editar.html'
    model = models.Egresso
    form_class = forms.EgressoForm
    success_url = reverse_lazy('gestao-egressos')

class RemoverEgressoView(DeleteView, GestaoRegrasMixin):
    model = models.Egresso
    success_url = reverse_lazy('gestao-egressos')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class VerEgressoView(DetailView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'egressos/ver.html'
    model = models.Egresso
