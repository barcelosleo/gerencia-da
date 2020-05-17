from django.urls import path
from siteda import views

urlpatterns = [
    path('<uuid:pk>/cadastro', views.CriarAssociado.as_view(), name="site-cadastro-associado")
]