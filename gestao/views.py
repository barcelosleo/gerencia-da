import datetime
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.urls import resolve
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from gestao.models import DiretorioAcademico, Area, Associado, Cargo
from gestao.forms import DiretorioAcademicoForm, AreaForm, CargoForm, DiretorCargoForm, AssociadoForm
import gestao.utilidades as utilidades

areas = [
    utilidades.Area('Direção Admnistrativa', 'gestao-administrativo', [
        utilidades.Ferramenta('Início', 'gestao-administrativo', 'home'),
        utilidades.Ferramenta('Config. Diretório', 'gestao-config-diretorio', 'settings'),
        utilidades.Ferramenta('Áreas', 'gestao-areas', 'view_carousel', [
            utilidades.SubFerramenta('gestao-areas-nova')
        ]),
        utilidades.Ferramenta('Cargos', 'gestao-cargos', 'contacts', [
            utilidades.SubFerramenta('gestao-cargos-novo'),
        ]),
        utilidades.Ferramenta('Diretores', 'gestao-diretores', 'people', [
            utilidades.SubFerramenta('gestao-diretores-cargos'),
        ]),
        utilidades.Ferramenta('Associados', 'gestao-associados', 'people_outline')
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
                diretorio = DiretorioAcademico.objects.get(pk=1)
                if diretorio.sigla:
                    request.session['sigla_diretorio'] = diretorio.sigla
                else:
                    request.session['sigla_diretorio'] = diretorio.nome

                if diretorio.logo:
                    request.session['logo_diretorio'] = diretorio.logo.url

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
        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ConfigurarDiretorioView(View):
    template_name = 'configurar_diretorio.html'
    def get(self, request, *args, **kwargs):
        diretorio = DiretorioAcademico.objects.get(pk=1)
        form = DiretorioAcademicoForm(instance=diretorio)

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        diretorio = DiretorioAcademico.objects.get(pk=1)
        form = DiretorioAcademicoForm(request.POST, request.FILES, instance=diretorio)

        if form.is_valid():
            print(form.cleaned_data['logo'])
            form.save()

            diretorio = DiretorioAcademico.objects.get(pk=1)

            request.session['sigla_diretorio'] = diretorio.sigla
            request.session['logo_diretorio'] = diretorio.logo.url

            return redirect(reverse('gestao-config-diretorio'))
        else:
            context = {
                'areas': areas,
                'area_ferramentas': areas[0].ferramentas,
                'nome_url': resolve(request.path_info).url_name,
                'form': form,
            }
            return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AreasView(View):
    template_name = 'areas/index.html'

    def get(self, request, *args, **kwargs):
        termo_pesquisa = request.GET.get('termo', None)

        if termo_pesquisa:
            lista_areas = Area.objects.filter(Q(nome__startswith=termo_pesquisa) | Q(gestor__nome__startswith=termo_pesquisa))
        else:
            lista_areas = Area.objects.all()

        paginator = Paginator(lista_areas, 5)

        page = request.GET.get('page', 1)

        try:
            areas_da = paginator.page(page)
        except PageNotAnInteger:
            areas_da = paginator.page(1)
        except EmptyPage:
            areas_da = paginator.page(paginator.num_pages)

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'areas_da': areas_da,
            'termo': termo_pesquisa,
        }

        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AreaView(View):
    template_name = 'areas/area.html'

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            area = Area.objects.get(pk=id)
            form = AreaForm(instance=area)
        else:
            form = AreaForm()

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'form': form,
            'id': id,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            area = Area.objects.get(pk=id)
            form = AreaForm(request.POST, instance=area)
        else:
            form = AreaForm(request.POST)

        if form.is_valid():
            associado = form.cleaned_data['gestor']
            area = form.save(commit=False)
            area.gestor = associado
            area.save()
            # form.save()
            return redirect(reverse('gestao-areas'))

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'form': form,
            'id': id,
        }
        return render(request, self.template_name, context)

    def delete(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            Area.objects.filter(pk=id).delete()

        return redirect(reverse('gestao-areas'))

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        if self.request.GET.get('method', None) == 'DELETE':
            return self.delete(self.request, *args, **kwargs)
        return super().dispatch(*args, **kwargs)

class CargosView(View):
    template_name = "cargos/index.html"

    def get(self, request, *args, **kwargs):
        termo_pesquisa = request.GET.get('termo', None)

        if termo_pesquisa:
            lista_cargos = Cargo.objects.filter(Q(nome__startswith=termo_pesquisa))
        else:
            lista_cargos = Cargo.objects.all()

        paginator = Paginator(lista_cargos, 5)

        page = request.GET.get('page', 1)

        try:
            cargos = paginator.page(page)
        except PageNotAnInteger:
            cargos = paginator.page(1)
        except EmptyPage:
            cargos = paginator.page(paginator.num_pages)

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'cargos': cargos,
            'termo': termo_pesquisa,
        }

        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class CargoView(View):
    template_name = 'cargos/cargo.html'

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            cargo = Cargo.objects.get(pk=id)
            form = CargoForm(instance=cargo)
        else:
            form = CargoForm()

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'form': form,
            'id': id,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            cargo = Cargo.objects.get(pk=id)
            form = CargoForm(request.POST, instance=cargo)
        else:
            form = CargoForm(request.POST)

        if form.is_valid():
            associados = form.cleaned_data['associados']
            cargo = form.save(commit=False)
            cargo.save()
            cargo.associados.clear()
            for associado in associados:
                cargo.associados.add(associado)
            cargo.save()
            # form.save()
            return redirect(reverse('gestao-cargos'))

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'form': form,
            'id': id,
        }
        return render(request, self.template_name, context)

    def delete(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            Cargo.objects.filter(pk=id).delete()

        return redirect(reverse('gestao-cargos'))

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        if self.request.GET.get('method', None) == 'DELETE':
            return self.delete(self.request, *args, **kwargs)
        return super().dispatch(*args, **kwargs)

class DiretoresView(View):
    template_name = "diretores/index.html"

    def get(self, request, *args, **kwargs):
        termo_pesquisa = request.GET.get('termo', None)

        if termo_pesquisa:
            diretores = Associado.objects.filter(Q(is_staff=True) & (Q(nome__startswith=termo_pesquisa) | Q(cargo__nome__startswith=termo_pesquisa)))
        else:
            diretores = Associado.objects.filter(is_staff=True)

        paginator = Paginator(diretores, 5)

        page = request.GET.get('page', 1)

        try:
            diretores = paginator.page(page)
        except PageNotAnInteger:
            diretores = paginator.page(1)
        except EmptyPage:
            diretores = paginator.page(paginator.num_pages)

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'diretores': diretores,
            'termo': termo_pesquisa,
        }

        return render(request, self.template_name, context)

    def delete(self, request, *args, **kwargs):
        pass

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        if self.request.GET.get('method', None) == 'DELETE':
            return self.delete(self.request, *args, **kwargs)
        return super().dispatch(*args, **kwargs)

class DiretorCargosView(View):
    template_name = 'diretores/cargos.html'

    def get(self, request, id, *args, **kwargs):
        diretor = Associado.objects.get(pk=id)
        initial = {
            'cargos': [cargo.id for cargo in diretor.cargos.all()]
        }
        form = DiretorCargoForm(initial=initial, instance=diretor)

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'form': form,
            'diretor': diretor,
        }
        return render(request, self.template_name, context)

    def post(self, request, id, *args, **kwargs):
        diretor = Associado.objects.get(pk=id)
        form = DiretorCargoForm(request.POST, instance=diretor)

        if form.is_valid():
            diretor.cargos.clear()
            for cargo in form.cleaned_data['cargos']:
                diretor.cargos.add(cargo)

            diretor.save()
            return redirect(reverse('gestao-diretores'))

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'form': form,
            'diretor': diretor,
        }
        return render(request, self.template_name, context)

    def delete(self, request, id, *args, **kwargs):
        diretor = Associado.objects.get(pk=id)
        if not diretor.is_superuser:
            diretor.cargos.clear()
            diretor.is_staff = False

        return redirect(reverse('gestao-diretores'))

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        if self.request.GET.get('method', None) == 'DELETE':
            id = kwargs['id']
            del kwargs['id']
            return self.delete(self.request, id, *args, **kwargs)
        return super().dispatch(*args, **kwargs)

class AssociadosView(View):
    template_name = 'associados/index.html'

    def get(self, request, *args, **kwargs):
        termo_pesquisa = request.GET.get('termo', None)

        if termo_pesquisa:
            associados = Associado.objects.filter(
                Q(nome__startswith=termo_pesquisa) |
                Q(sobrenome__startswith=termo_pesquisa) |
                Q(email__startswith=termo_pesquisa) |
                Q(telefone__startswith=termo_pesquisa) |
                Q(matricula__startswith=termo_pesquisa)
            )
        else:
            associados = Associado.objects.all()

        paginator = Paginator(associados, 5)

        page = request.GET.get('page', 1)

        try:
            associados = paginator.page(page)
        except PageNotAnInteger:
            associados = paginator.page(1)
        except EmptyPage:
            associados = paginator.page(paginator.num_pages)

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'associados': associados,
            'termo': termo_pesquisa,
        }

        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        # if self.request.GET.get('method', None) == 'DELETE':
        #     id = kwargs['id']
        #     del kwargs['id']
        #     return self.delete(self.request, id, *args, **kwargs)
        return super().dispatch(*args, **kwargs)

class AssociadoView(View):
    template_name = 'associados/associado.html'

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            associado = Associado.objects.get(pk=id)
            form = AssociadoForm(instance=associado)
        else:
            form = AssociadoForm()

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'form': form,
            'id': id,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            associado = Associado.objects.get(pk=id)
            form = AssociadoForm(request.POST, instance=associado)
        else:
            form = AssociadoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('gestao-associados'))

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'form': form,
            'id': id,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        # if self.request.GET.get('method', None) == 'DELETE':
        #     id = kwargs['id']
        #     del kwargs['id']
        #     return self.delete(self.request, id, *args, **kwargs)
        return super().dispatch(*args, **kwargs)


class EventosView(View):
    template_name = 'eventos.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class FinancasView(View):
    template_name = 'financas.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
