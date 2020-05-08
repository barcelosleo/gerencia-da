import datetime
import random
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.urls import resolve
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from . import models
from . import forms
from .utilidades import areas

class BaseView(LoginRequiredMixin, View):
    login_url = '/gestao/login'


class GestorLoginView(BaseView):
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

                try:
                    diretorio = models.DiretorioAcademico.objects.get(pk=1)
                except models.DiretorioAcademico.DoesNotExist:
                    return redirect(reverse('gestao-config-diretorio'))

                if diretorio.sigla:
                    request.session['sigla_diretorio'] = diretorio.sigla
                else:
                    request.session['sigla_diretorio'] = diretorio.nome

                if diretorio.logo:
                    request.session['logo_diretorio'] = diretorio.logo.url

                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))

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

class GestorHomeView(BaseView):
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

class ConfigurarDiretorioView(BaseView):
    template_name = 'configurar_diretorio.html'
    def get(self, request, *args, **kwargs):
        try:
            diretorio = models.DiretorioAcademico.objects.get(pk=1)
            form = forms.DiretorioAcademicoForm(instance=diretorio)
        except models.DiretorioAcademico.DoesNotExist:
            form = forms.DiretorioAcademicoForm()

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            diretorio = models.DiretorioAcademico.objects.get(pk=1)
            form = forms.DiretorioAcademicoForm(request.POST, request.FILES, instance=diretorio)
        except models.DiretorioAcademico.DoesNotExist:
            form = forms.DiretorioAcademicoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            diretorio = models.DiretorioAcademico.objects.get(pk=1)

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

class AreasView(BaseView):
    template_name = 'areas/index.html'

    def get(self, request, *args, **kwargs):
        termo_pesquisa = request.GET.get('termo', None)

        if termo_pesquisa:
            lista_areas = models.Area.objects.filter(Q(nome__startswith=termo_pesquisa) | Q(gestor__nome__startswith=termo_pesquisa))
        else:
            lista_areas = models.Area.objects.all()

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

class AreaView(BaseView):
    template_name = 'areas/area.html'

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            area = models.Area.objects.get(pk=id)
            form = forms.AreaForm(instance=area)
        else:
            form = forms.AreaForm()

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
            area = models.Area.objects.get(pk=id)
            form = forms.AreaForm(request.POST, instance=area)
        else:
            form = forms.AreaForm(request.POST)

        if form.is_valid():
            associado = form.cleaned_data['gestor']
            area = form.save(commit=False)
            area.gestor = associado
            area.save()
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
            models.Area.objects.filter(pk=id).delete()

        return redirect(reverse('gestao-areas'))

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        if self.request.GET.get('method', None) == 'DELETE':
            return self.delete(self.request, *args, **kwargs)
        return super().dispatch(*args, **kwargs)

class CargosView(BaseView):
    template_name = "cargos/index.html"

    def get(self, request, *args, **kwargs):
        termo_pesquisa = request.GET.get('termo', None)

        if termo_pesquisa:
            lista_cargos = models.Cargo.objects.filter(Q(nome__startswith=termo_pesquisa))
        else:
            lista_cargos = models.Cargo.objects.all()

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

class CargoView(BaseView):
    template_name = 'cargos/cargo.html'

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            cargo = models.Cargo.objects.get(pk=id)
            form = forms.CargoForm(instance=cargo)
        else:
            form = forms.CargoForm()

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
            cargo = models.Cargo.objects.get(pk=id)
            form = forms.CargoForm(request.POST, instance=cargo)
        else:
            form = forms.CargoForm(request.POST)

        if form.is_valid():
            associados = form.cleaned_data['associados']
            cargo = form.save(commit=False)
            cargo.save()
            cargo.associados.clear()
            for associado in associados:
                cargo.associados.add(associado)
            cargo.save()
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
            models.Cargo.objects.filter(pk=id).delete()

        return redirect(reverse('gestao-cargos'))

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        if self.request.GET.get('method', None) == 'DELETE':
            return self.delete(self.request, *args, **kwargs)
        return super().dispatch(*args, **kwargs)

class DiretoresView(BaseView):
    template_name = "diretores/index.html"

    def get(self, request, *args, **kwargs):
        termo_pesquisa = request.GET.get('termo', None)

        if termo_pesquisa:
            diretores = models.Associado.objects.filter(Q(is_staff=True) & (Q(nome__startswith=termo_pesquisa) | Q(cargo__nome__startswith=termo_pesquisa)))
        else:
            diretores = models.Associado.objects.filter(is_staff=True)

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

class DiretorCargosView(BaseView):
    template_name = 'diretores/cargos.html'

    def get(self, request, id, *args, **kwargs):
        diretor = models.Associado.objects.get(pk=id)
        initial = {
            'cargos': [cargo.id for cargo in diretor.cargos.all()]
        }
        form = forms.DiretorCargoForm(initial=initial, instance=diretor)

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'form': form,
            'diretor': diretor,
        }
        return render(request, self.template_name, context)

    def post(self, request, id, *args, **kwargs):
        diretor = models.Associado.objects.get(pk=id)
        form = forms.DiretorCargoForm(request.POST, instance=diretor)

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
        diretor = models.Associado.objects.get(pk=id)
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

class AssociadosView(BaseView):
    template_name = 'associados/index.html'

    def get(self, request, *args, **kwargs):
        termo_pesquisa = request.GET.get('termo', None)

        if termo_pesquisa:
            associados = models.Associado.objects.filter(
                Q(is_active=True) &
                (
                    Q(nome__startswith=termo_pesquisa) |
                    Q(sobrenome__startswith=termo_pesquisa) |
                    Q(email__startswith=termo_pesquisa) |
                    Q(telefone__startswith=termo_pesquisa) |
                    Q(matricula__startswith=termo_pesquisa)
                )
            )
        else:
            associados = models.Associado.objects.filter(
                is_active=True
            )

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

class AssociadoView(BaseView):
    template_name = 'associados/associado.html'

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            associado = models.Associado.objects.get(pk=id)
            form = forms.AssociadoForm(instance=associado)
        else:
            form = forms.AssociadoForm()

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
            associado = models.Associado.objects.get(pk=id)
            form = forms.AssociadoForm(request.POST, request.FILES, instance=associado)
        else:
            form = forms.AssociadoForm(request.POST, request.FILES)

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

    def delete(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            models.Associado.objects.filter(pk=id).delete()

        return redirect(reverse('gestao-associados'))

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        if self.request.GET.get('method', None) == 'DELETE':
            return self.delete(self.request, *args, **kwargs)
        return super().dispatch(*args, **kwargs)

class EgressosView(BaseView):
    template_name = 'egressos/index.html'

    def get(self, request, *args, **kwargs):
        termo_pesquisa = request.GET.get('termo', None)

        if termo_pesquisa:
            associados = models.Associado.objects.filter(
                Q(is_active=False) &
                (
                    Q(nome__startswith=termo_pesquisa) |
                    Q(sobrenome__startswith=termo_pesquisa) |
                    Q(email__startswith=termo_pesquisa) |
                    Q(telefone__startswith=termo_pesquisa) |
                    Q(matricula__startswith=termo_pesquisa)
                )
            )
        else:
            associados = models.Associado.objects.filter(
                is_active=False
            )

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

class EgressoView(BaseView):
    template_name = 'egressos/egresso.html'

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            associado = models.Associado.objects.get(pk=id)
            form = forms.EgressoForm(instance=associado)
        else:
            form = forms.EgressoForm()

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
            associado = models.Associado.objects.get(pk=id)
            form = forms.EgressoForm(request.POST, request.FILES, instance=associado)
        else:
            random.seed(datetime.datetime.now())

            form = forms.EgressoForm(request.POST, request.FILES)


        if form.is_valid():
            matricula_randomica = str(int(random.random() * 1e17))

            egresso = form.save(commit=False)
            egresso.matricula = 'EGR' + matricula_randomica + "".join(random.sample(egresso.nome.strip(), 3)).upper()
            egresso.is_staff = False
            egresso.is_active = False
            egresso.save()
            return redirect(reverse('gestao-egressos'))


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
            models.Associado.objects.filter(pk=id).delete()

        return redirect(reverse('gestao-egressos'))

    def dispatch(self, *args, **kwargs):
        if self.request.GET.get('method', None) == 'DELETE':
            return self.delete(self.request, *args, **kwargs)
        return super().dispatch(*args, **kwargs)

class AtasView(BaseView):
    template_name = 'atas/index.html'

    def get(self, request, *args, **kwargs):
        termo_pesquisa = request.GET.get('termo', None)

        if termo_pesquisa:
            atas = models.Reuniao.objects.filter(Q(data__startswith=termo_pesquisa))
        else:
            atas = models.Reuniao.objects.all()

        paginator = Paginator(atas, 5)

        page = request.GET.get('page', 1)

        try:
            atas = paginator.page(page)
        except PageNotAnInteger:
            atas = paginator.page(1)
        except EmptyPage:
            atas = paginator.page(paginator.num_pages)

        context = {
            'areas': areas,
            'area_ferramentas': areas[0].ferramentas,
            'nome_url': resolve(request.path_info).url_name,
            'atas': atas,
            'termo': termo_pesquisa,
        }

        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="/gestao/login"))
    def dispatch(self, *args, **kwargs):
        # if self.request.GET.get('method', None) == 'DELETE':
        #     return self.delete(self.request, *args, **kwargs)
        return super().dispatch(*args, **kwargs)

class AtaView(BaseView):
    template_name = 'atas/ata.html'

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id:
            reuniao = models.Reuniao.objects.get(pk=id)
            form = forms.ReuniaoForm(instance=reuniao)
        else:
            form = forms.ReuniaoForm(initial={
                'ata': "Transcrição de ata..."
            })

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
            reuniao = models.Reuniao.objects.get(pk=id)
            form = forms.ReuniaoForm(request.POST, instance=reuniao)
        else:
            form = forms.ReuniaoForm(request.POST)


        if form.is_valid():
            presentes = form.cleaned_data['presentes']
            reuniao = form.save(commit=False)
            reuniao.save()
            reuniao.presentes.clear()

            for presente in presentes:
                reuniao.presentes.add(presente)

            reuniao.save()

            return redirect(reverse('gestao-reunioes'))


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
            models.Reuniao.objects.filter(pk=id).delete()

        return redirect(reverse('gestao-reunioes'))

    def see(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        reuniao = models.Reuniao.objects.get(pk=id)
        response = {
            'id': id,
            'data': reuniao.data,
            'titulo': reuniao.titulo,
            'presentes': [associado.nome for associado in reuniao.presentes.all()],
            'ata': reuniao.ata
        }
        return JsonResponse(response)


    def dispatch(self, *args, **kwargs):
        if self.request.GET.get('method', None) == 'DELETE':
            return self.delete(self.request, *args, **kwargs)
        if self.request.GET.get('method', None) == 'SEE':
            return self.see(self.request, *args, **kwargs)
        return super().dispatch(*args, **kwargs)

class GruposView(BaseView):
    pass