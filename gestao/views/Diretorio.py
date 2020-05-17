from django.urls import reverse_lazy

from django.views.generic.edit import UpdateView

from gestao import models
from gestao import forms

from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin, GestaoPermissoesMixin

class ConfigurarDiretorioView(UpdateView, GestaoRegrasMixin, GestaoPermissoesMixin, GestaoContextMixin):
    template_name = 'diretorio/form.html'
    form_class = forms.DiretorioAcademicoForm
    success_url = reverse_lazy('gestao-config-diretorio')
    permission_required = ('gestao.change_diretorioacademico', 'gestao.view_diretorioacademico')

    def form_valid(self, form):
        self.object = form.save()

        self.request.session['sigla_diretorio'] = self.object.sigla
        self.request.session['logo_diretorio'] = self.object.logo.url

        return super().form_valid(form)

    def get_object(self):
        try:
            return models.DiretorioAcademico.objects.get(pk=1)
        except models.DiretorioAcademico.DoesNotExist:
            return models.DiretorioAcademico()