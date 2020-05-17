from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy

from django.views import View
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm

from gestao import models
from gestao import forms

from gestao.mixins import GestaoRegrasMixin, GestaoContextMixin

class LoginGestor(LoginView):
    template_name = 'gestor/login.html'
    form = AuthenticationForm
    redirect_authenticated_user = True
    extra_context = {
        'next': reverse_lazy('gestao-administrativo'),
    }

    def get_success_url(self):
        try:
            diretorio = models.DiretorioAcademico.objects.get(pk=1)
            self.request.session['sigla_diretorio'] = diretorio.sigla
            self.request.session['logo_diretorio'] = diretorio.logo.url
        except models.DiretorioAcademico.DoesNotExist:
            pass
        return super().get_success_url()


class LogoutGestor(LogoutView):
    next_page = reverse_lazy('gestao-login')

class GestorHomeView(DetailView, GestaoRegrasMixin, GestaoContextMixin):
    template_name = 'gestor/index.html'
    model = models.Diretor

    def get_object(self):
        return self.request.user