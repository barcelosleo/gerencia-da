from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, ModelFormMixin, ProcessFormView
from django.views.generic.detail import DetailView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password

from gestao import models
from . import forms

class CriarAssociado(DetailView, ModelFormMixin, ProcessFormView):
    template_name = 'site/novo_associado.html'
    model = models.LinkCadastro
    save_model = models.Associado
    success_url = reverse_lazy('gestao-login')

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if timezone.now() > self.object.validade or self.object.usado:
            raise PermissionDenied

        context = self.get_context_data(object=self.object)
        context['tipo_usuario'] = self.object.tipo_usuario
        return self.render_to_response(context)

    def get_form_class(self):
        link_cadastro = self.get_object()

        self.form_class = forms.AlunoForm

        if link_cadastro.tipo_usuario == models.LinkCadastro.TipoUsuario.DIRETOR:
            self.form_class = forms.DiretorForm
            self.save_model = models.Diretor
        elif link_cadastro.tipo_usuario == models.LinkCadastro.TipoUsuario.ALUNO:
            self.form_class = forms.AlunoForm
            self.save_model = models.Aluno

        return super().get_form_class()

    def form_valid(self, form):
        link_cadastro = self.get_object()
        link_cadastro.usado = True
        link_cadastro.save()

        cleaned_data = form.cleaned_data
        del cleaned_data['password_confirm']

        cleaned_data['password'] = make_password(cleaned_data['password'])

        self.save_model.objects.create(**cleaned_data)

        return HttpResponseRedirect(self.success_url)