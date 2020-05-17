from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from gestao import models
from gestao import forms

from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin, GestaoPermissoesMixin

class AreaListView(ListView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'areas/index.html'
    model = models.Area
    paginate_by = 5

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        context = models.Area.objects.filter(Q(nome__startswith=termo_pesquisa) | Q(gestor__nome__startswith=termo_pesquisa))
        return context

class CriarAreaView(CreateView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'areas/nova.html'
    model = models.Area
    form_class = forms.AreaForm
    success_url = reverse_lazy('gestao-areas')
    permission_required = 'gestao.add_area'

class EditarAreaView(UpdateView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'areas/editar.html'
    model = models.Area
    form_class = forms.AreaForm
    success_url = reverse_lazy('gestao-areas')
    permission_required = 'gestao.change_area'

class RemoverAreaView(DeleteView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    model = models.Area
    success_url = reverse_lazy('gestao-areas')
    permission_required = 'gestao.delete_area'

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return self.post(request, *args, **kwargs)
