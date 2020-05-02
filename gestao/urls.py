from django.urls import path
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .views import (
    GestorLoginView,
    GestorHomeView,
    EventosView,
    FinancasView,
    ConfigurarDiretorioView,
    AreasView,
    AreaView,
    CargosView,
    CargoView,
    DiretoresView,
    DiretorCargosView,
    AssociadosView,
    AssociadoView,
)

def deslogar(request):
    logout(request)
    return redirect("/gestao/login")

urlpatterns = [
    path('', GestorHomeView.as_view(), name="gestao-administrativo"),
    path('login/', GestorLoginView.as_view(), name="gestao-login"),
    path('logout/', deslogar, name="gestao-logout"),
    path('eventos/', EventosView.as_view(), name="gestao-eventos"),
    path('financas/', FinancasView.as_view(), name="gestao-financeira"),
    path('configurar-diretorio/', ConfigurarDiretorioView.as_view(), name="gestao-config-diretorio"),
    path('areas/', AreasView.as_view(), name="gestao-areas"),
    path('area/', AreaView.as_view(), name="gestao-areas-nova"),
    path('cargos', CargosView.as_view(), name="gestao-cargos"),
    path('cargo/', CargoView.as_view(), name="gestao-cargos-novo"),
    path('diretores/', DiretoresView.as_view(), name="gestao-diretores"),
    path('diretores/<int:id>/cargos', DiretorCargosView.as_view(), name="gestao-diretores-cargos"),
    path('associados/', AssociadosView.as_view(), name="gestao-associados"),
    path('associado/', AssociadoView.as_view(), name="gestao-associados-novo"),
]