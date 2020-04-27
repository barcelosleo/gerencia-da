from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.urls import resolve

from gestao.models import Gestor, DiretorioAcademico
from gestao.forms import DiretorioAcademicoForm
import gestao.utilidades as utilidades

areas = [
    utilidades.Area('Direção Admnistrativa', 'gestao-administrativo', [
        utilidades.Ferramenta('Início', 'gestao-administrativo', 'home'),
        utilidades.Ferramenta('Config. Diretório', 'gestao-config-diretorio', 'settings'),
        utilidades.Ferramenta('Áreas', 'gestao-logout', 'view_carousel'),
        utilidades.Ferramenta('Gestores', 'gestao-logout', 'people'),
        utilidades.Ferramenta('Associados', 'gestao-logout', 'people_outline')
    ]),
    utilidades.Area('Financeiro', 'gestao-financeira', []),
    utilidades.Area('Eventos', 'gestao-eventos', []),
]

class GestorLoginView(View):
    template_name = 'gestor_login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        matricula = request.POST['matricula']
        senha = request.POST['senha']

        associado = authenticate(request, matricula=matricula, password=senha)

        if associado is not None:
            if associado.is_staff:
                login(request, associado)
                return redirect("/gestao/")
            else:
                return render(request, self.template_name, {
                    'erro_validacao': 'O associado não é parte da Administração do Diretório Acadêmico',
                    'matricula': matricula
                })
        else:
            return render(request, self.template_name, {
                'erro_validacao': 'Não foi possível fazer login! Verifique sua matrícula e/ou senha...',
                'matricula': matricula
            })

class GestorHomeView(View):
    template_name = 'gestor_home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name
        })

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ConfigurarDiretorioView(View):
    template_name = 'configurar_diretorio.html'
    def get(self, request, *args, **kwargs):
        diretorio = DiretorioAcademico.objects.get(pk=1)
        form = DiretorioAcademicoForm()
        return render(request, self.template_name, {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'diretorio': diretorio,
            'form': form,
        })

class EventosView(View):
    template_name = 'eventos.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class FinancasView(View):
    template_name = 'financas.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
