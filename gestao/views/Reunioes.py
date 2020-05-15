from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from gestao import models
from gestao import forms

from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin

class ReuniaoListView(ListView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'atas/index.html'
    model = models.Reuniao
    paginate_by = 5

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        context = models.Reuniao.objects.filter(
            Q(data__startswith=termo_pesquisa) | Q(titulo__startswith=termo_pesquisa)
        )
        return context

class CriarReuniaoView(CreateView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'atas/nova.html'
    model = models.Reuniao
    form_class = forms.ReuniaoForm
    success_url = reverse_lazy('gestao-reunioes')

class EditarReuniaoView(UpdateView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'atas/editar.html'
    model = models.Reuniao
    form_class = forms.ReuniaoForm
    success_url = reverse_lazy('gestao-reunioes')

class RemoverReuniaoView(DeleteView, GestaoRegrasMixin):
    model = models.Reuniao
    success_url = reverse_lazy('gestao-reunioes')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class VerReuniaoView(DetailView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'atas/ver.html'
    model = models.Reuniao
