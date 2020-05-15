from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from gestao import models
from gestao import forms

from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin

class DiretorListView(ListView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'diretores/index.html'
    model = models.Diretor
    paginate_by = 5

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        context = models.Diretor.objects.filter(
            Q(nome__startswith=termo_pesquisa) |
            Q(sobrenome__startswith=termo_pesquisa) |
            Q(email__startswith=termo_pesquisa) |
            Q(telefone__startswith=termo_pesquisa) |
            Q(matricula__startswith=termo_pesquisa)
        )
        return context

class CriarDiretorView(CreateView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'diretores/novo.html'
    model = models.Associado
    form_class = forms.AssociadoForm
    success_url = reverse_lazy('gestao-diretores')

    def form_valid(self, form):
        models.Diretor.objects.create(**form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())

class EditarDiretorView(UpdateView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'diretores/editar.html'
    model = models.Diretor
    form_class = forms.DiretorCargoForm
    success_url = reverse_lazy('gestao-diretores')

class RemoverDiretorView(DeleteView, GestaoRegrasMixin):
    model = models.Diretor
    success_url = reverse_lazy('gestao-diretores')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_staff = False
        self.object.save()

        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

class VerDiretorView(DetailView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'diretores/ver.html'
    model = models.Diretor
