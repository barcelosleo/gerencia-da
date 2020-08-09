from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from financeiro.mixins import FinanceiroMixin, FinanceiroProtegidoMixin

from financeiro.models import TemporadaEncomenda


class ListTemporadaEncomendaView(ListView, FinanceiroMixin):
    template_name = 'temporada_encomendas/index.html'
    model = TemporadaEncomenda
    paginate_by = 5
    ordering = ('id',)

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        queryset = self.model.objects.filter(
            Q(data__startswith=termo_pesquisa)
        )

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


class CriarTemporadaEncomendaView(CreateView, FinanceiroProtegidoMixin):
    template_name = "temporada_encomendas/form.html"
    model = TemporadaEncomenda
    success_url = reverse_lazy('financeiro-temporada-encomendas')
    permission_required = 'financeiro.add_temporadaencomenda'
    fields = ('data', 'data_fim', 'produtos')


class EditarTemporadaEncomendaView(UpdateView, FinanceiroProtegidoMixin):
    template_name = "temporada_encomendas/form.html"
    model = TemporadaEncomenda
    success_url = reverse_lazy('financeiro-temporada-encomendas')
    permission_required = 'financeiro.change_temporadaencomenda'
    fields = ('data', 'data_fim', 'produtos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Editar"
        return context


class RemoverTemporadaEncomendaView(DeleteView, FinanceiroProtegidoMixin):
    model = TemporadaEncomenda
    success_url = reverse_lazy('financeiro-temporada-encomendas')
    permission_required = 'financeiro.delete_temporadaencomenda'

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return self.post(request, *args, **kwargs)


class VerTemporadaEncomendaView(DetailView, FinanceiroProtegidoMixin):
    template_name = "temporada_encomendas/ver.html"
    model = TemporadaEncomenda
    permission_required = 'financeiro.view_temporadaencomenda'
