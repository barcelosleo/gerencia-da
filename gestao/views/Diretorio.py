from django.urls import reverse_lazy

from django.views.generic.edit import UpdateView

from gestao import models
from gestao import forms

from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin

class ConfigurarDiretorioView(UpdateView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'diretorio/form.html'
    form_class = forms.DiretorioAcademicoForm
    success_url = reverse_lazy('gestao-config-diretorio')

    def form_valid(self, form):
        self.object = form.save()

        self.request.session['sigla_diretorio'] = self.object.sigla
        self.request.session['logo_diretorio'] = self.object.logo.url

        return super().form_valid(form)

    def get_object(self):
        return models.DiretorioAcademico.objects.get(pk=1)