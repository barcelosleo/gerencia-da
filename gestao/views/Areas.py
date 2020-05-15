from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from gestao import models
from gestao import forms

from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin

class AreaListView(ListView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'areas/index.html'
    model = models.Area
    paginate_by = 5

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        context = models.Area.objects.filter(Q(nome__startswith=termo_pesquisa) | Q(gestor__nome__startswith=termo_pesquisa))
        return context

class CriarAreaView(CreateView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'areas/nova.html'
    model = models.Area
    form_class = forms.AreaForm
    success_url = reverse_lazy('gestao-areas')

class EditarAreaView(UpdateView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'areas/editar.html'
    model = models.Area
    form_class = forms.AreaForm
    success_url = reverse_lazy('gestao-areas')

class RemoverAreaView(DeleteView, GestaoRegrasMixin):
    model = models.Area
    success_url = reverse_lazy('gestao-areas')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
