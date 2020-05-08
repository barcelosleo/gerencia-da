from django.urls import path, include
from django.contrib.auth import logout
from django.shortcuts import redirect, reverse

from . import views

def deslogar(request):
    logout(request)
    return redirect(reverse('gestao-login'))

urlpatterns = [
    path('', views.GestorHomeView.as_view(), name="gestao-administrativo"),
    # path('', include('django.contrib.auth.urls')),
    path('login/', views.GestorLoginView.as_view(), name="gestao-login"),
    path('logout/', deslogar, name="gestao-logout"),
    path('configurar-diretorio/', views.ConfigurarDiretorioView.as_view(), name="gestao-config-diretorio"),
    path('areas/', views.AreasView.as_view(), name="gestao-areas"),
    path('area/', views.AreaView.as_view(), name="gestao-areas-nova"),
    path('cargos', views.CargosView.as_view(), name="gestao-cargos"),
    path('cargo/', views.CargoView.as_view(), name="gestao-cargos-novo"),
    path('diretores/', views.DiretoresView.as_view(), name="gestao-diretores"),
    path('diretores/<int:id>/cargos', views.DiretorCargosView.as_view(), name="gestao-diretores-cargos"),
    path('associados/', views.AssociadosView.as_view(), name="gestao-associados"),
    path('associado/', views.AssociadoView.as_view(), name="gestao-associados-novo"),
    path('egressos/', views.EgressosView.as_view(), name="gestao-egressos"),
    path('egresso/', views.EgressoView.as_view(), name="gestao-egressos-novo"),
    path('reunioes/', views.AtasView.as_view(), name="gestao-reunioes"),
    path('reuniao/', views.AtaView.as_view(), name="gestao-reunioes-nova"),
]