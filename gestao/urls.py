from django.urls import path
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .views import GestorLoginView, GestorHomeView, EventosView, FinancasView, ConfigurarDiretorioView

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
]