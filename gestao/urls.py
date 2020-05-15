from django.urls import path

from gestao import views

urlpatterns = [
    path('login/', views.LoginGestor.as_view(), name="gestao-login"),
    path('logout/', views.LogoutGestor.as_view(), name="gestao-logout"),

    path('home/', views.GestorHomeView.as_view(), name="gestao-administrativo"),

    path('reunioes/', views.ReuniaoListView.as_view(), name="gestao-reunioes"),
    path('reuniao/', views.CriarReuniaoView.as_view(), name="gestao-reunioes-nova"),
    path('reuniao/<int:pk>', views.EditarReuniaoView.as_view(), name="gestao-reunioes-editar"),
    path('reuniao/<int:pk>/remover', views.RemoverReuniaoView.as_view(), name="gestao-reunioes-remover"),
    path('reuniao/<int:pk>/ver', views.VerReuniaoView.as_view(), name="gestao-reunioes-ver"),

    path('alunos/', views.AssociadoListView.as_view(), name="gestao-associados"),
    path('aluno/', views.CriarAssociadoView.as_view(), name="gestao-associados-novo"),
    path('aluno/<int:pk>', views.EditarAssociadoView.as_view(), name="gestao-associados-editar"),
    path('aluno/<int:pk>/remover', views.RemoverAssociadoView.as_view(), name="gestao-associados-remover"),
    path('aluno/<int:pk>/ver', views.VerAssociadoView.as_view(), name="gestao-associados-ver"),

    path('egressos/', views.EgressoListView.as_view(), name="gestao-egressos"),
    path('egresso/', views.CriarEgressoView.as_view(), name="gestao-egressos-novo"),
    path('egresso/<int:pk>', views.EditarEgressoView.as_view(), name="gestao-egressos-editar"),
    path('egresso/<int:pk>/remover', views.RemoverEgressoView.as_view(), name="gestao-egressos-remover"),
    path('egresso/<int:pk>/ver', views.VerEgressoView.as_view(), name="gestao-egressos-ver"),

    path('grupos/', views.GrupoListView.as_view(), name="gestao-grupos"),
    path('grupo/', views.CriarGrupoView.as_view(), name="gestao-grupos-novo"),
    path('grupo/<int:pk>', views.EditarGrupoView.as_view(), name="gestao-grupos-editar"),
    path('grupo/<int:pk>/remover', views.RemoverGrupoView.as_view(), name="gestao-grupos-remover"),
    path('grupo/<int:pk>/ver', views.VerGrupoView.as_view(), name="gestao-grupos-ver"),
    path('grupo/<int:pk>/permissoes', views.GerenciarPermissoesView.as_view(), name="gestao-grupos-permissoes"),

    path('areas/', views.AreaListView.as_view(), name="gestao-areas"),
    path('area/', views.CriarAreaView.as_view(), name="gestao-areas-nova"),
    path('area/<int:pk>', views.EditarAreaView.as_view(), name="gestao-areas-editar"),
    path('area/<int:pk>/remover', views.RemoverAreaView.as_view(), name="gestao-areas-remover"),

    path('diretores/', views.DiretorListView.as_view(), name="gestao-diretores"),
    path('diretor/', views.CriarDiretorView.as_view(), name="gestao-diretores-novo"),
    path('diretor/<int:pk>', views.EditarDiretorView.as_view(), name="gestao-diretores-editar"),
    path('diretor/<int:pk>/remover', views.RemoverDiretorView.as_view(), name="gestao-diretores-remover"),
    path('diretor/<int:pk>/ver', views.VerDiretorView.as_view(), name="gestao-diretores-ver"),

    path('configurar-diretorio/', views.ConfigurarDiretorioView.as_view(), name="gestao-config-diretorio"),
]