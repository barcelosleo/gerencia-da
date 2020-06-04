from django.urls import path

from financeiro.views import (
        Carteiras,
        InicioFinanceiro,
        EntradasFinanceiras,
        SaidasFinanceiras,
        TransferenciasFinanceiras,
        Produtos,
        Vendas
    )

urlpatterns = [
    path('inicio/', InicioFinanceiro.InicioFinanceiroView.as_view(), name="financeiro-inicio"),

    path('carteiras/', Carteiras.ListCarteiraView.as_view(), name="financeiro-carteiras"),
    path('carteira/', Carteiras.CriarCarteiraView.as_view(), name="financeiro-carteiras-nova"),
    path('carteira/<int:pk>/', Carteiras.EditarCarteiraView.as_view(), name="financeiro-carteiras-editar"),
    path('carteira/<int:pk>/remover', Carteiras.RemoverCarteiraView.as_view(), name="financeiro-carteiras-remover"),
    path('carteira/<int:pk>/ver', Carteiras.VerCarteiraView.as_view(), name="financeiro-carteiras-ver"),

    path('entradas/', EntradasFinanceiras.ListEntradaFinanceiraView.as_view(), name="financeiro-entradas"),
    path('entrada/', EntradasFinanceiras.CriarEntradaFinanceiraView.as_view(), name="financeiro-entradas-nova"),
    path('entrada/<int:pk>/', EntradasFinanceiras.EditarEntradaFinanceiraView.as_view(), name="financeiro-entradas-editar"),
    path('entrada/<int:pk>/remover', EntradasFinanceiras.RemoverEntradaFinanceiraView.as_view(), name="financeiro-entradas-remover"),
    path('entrada/<int:pk>/ver', EntradasFinanceiras.VerEntradaFinanceiraView.as_view(), name="financeiro-entradas-ver"),

    path('saidas/', SaidasFinanceiras.ListSaidaFinanceiraView.as_view(), name="financeiro-saidas"),
    path('saida/', SaidasFinanceiras.CriarSaidaFinanceiraView.as_view(), name="financeiro-saidas-nova"),
    path('saida/<int:pk>/', SaidasFinanceiras.EditarSaidaFinanceiraView.as_view(), name="financeiro-saidas-editar"),
    path('saida/<int:pk>/remover', SaidasFinanceiras.RemoverSaidaFinanceiraView.as_view(), name="financeiro-saidas-remover"),
    path('saida/<int:pk>/ver', SaidasFinanceiras.VerSaidaFinanceiraView.as_view(), name="financeiro-saidas-ver"),

    path('transferencias/', TransferenciasFinanceiras.ListTransferenciaFinanceiraView.as_view(), name="financeiro-transferencias"),
    path('transferencia/', TransferenciasFinanceiras.CriarTransferenciaFinanceiraView.as_view(), name="financeiro-transferencias-nova"),
    path('transferencia/<int:pk>/', TransferenciasFinanceiras.EditarTransferenciaFinanceiraView.as_view(), name="financeiro-transferencias-editar"),
    path('transferencia/<int:pk>/remover', TransferenciasFinanceiras.RemoverTransferenciaFinanceiraView.as_view(), name="financeiro-transferencias-remover"),
    path('transferencia/<int:pk>/ver', TransferenciasFinanceiras.VerTransferenciaFinanceiraView.as_view(), name="financeiro-transferencias-ver"),

    path('produtos/', Produtos.ListProdutoView.as_view(), name="financeiro-produtos"),
    path('produto/', Produtos.CriarProdutoView.as_view(), name="financeiro-produtos-novo"),
    path('produto/<int:pk>/', Produtos.EditarProdutoView.as_view(), name="financeiro-produtos-editar"),
    path('produto/<int:pk>/remover', Produtos.RemoverProdutoView.as_view(), name="financeiro-produtos-remover"),
    path('produto/<int:pk>/ver', Produtos.VerProdutoView.as_view(), name="financeiro-produtos-ver"),

    path('vendas/', Vendas.ListVendaView.as_view(), name="financeiro-vendas"),
    path('venda/', Vendas.CriarVendaView.as_view(), name="financeiro-vendas-nova"),
    path('venda/<int:pk>/', Vendas.EditarVendaView.as_view(), name="financeiro-vendas-editar"),
    path('venda/<int:pk>/remover', Vendas.RemoverVendaView.as_view(), name="financeiro-vendas-remover"),
    path('venda/<int:pk>/ver', Vendas.VerVendaView.as_view(), name="financeiro-vendas-ver"),
    path('venda/<int:pk>/parcelas', Vendas.ParcelasVenda.as_view(), name="financeiro-vendas-parcelas"),
]