from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from financeiro.mixins import FinanceiroMixin, FinanceiroProtegidoMixin

from financeiro.models import Encomenda


class ListEncomendaView(ListView, FinanceiroMixin):
    template_name = 'encomendas/index.html'
    model = Encomenda
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


class CriarEncomendaView(CreateView, FinanceiroProtegidoMixin):
    template_name = "encomendas/form.html"
    model = Encomenda
    success_url = reverse_lazy('financeiro-temporada-encomendas')
    permission_required = 'financeiro.add_enconmenda'
    fields = ('data', 'associado', 'temporada_encomenda', 'produtos')


class EditarEncomendaView(UpdateView, FinanceiroProtegidoMixin):
    template_name = "encomendas/form.html"
    model = Encomenda
    success_url = reverse_lazy('financeiro-temporada-encomendas')
    permission_required = 'financeiro.change_enconmenda'
    fields = ('data', 'associado', 'temporada_encomenda', 'produtos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Editar"
        return context


class RemoverEncomendaView(DeleteView, FinanceiroProtegidoMixin):
    model = Encomenda
    success_url = reverse_lazy('financeiro-temporada-encomendas')
    permission_required = 'financeiro.delete_enconmenda'

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return self.post(request, *args, **kwargs)


class VerEncomendaView(DetailView, FinanceiroProtegidoMixin):
    template_name = "encomendas/ver.html"
    model = Encomenda
    permission_required = 'financeiro.view_enconmenda'
