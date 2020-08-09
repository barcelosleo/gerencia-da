from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from financeiro.mixins import FinanceiroMixin, FinanceiroProtegidoMixin

from financeiro.models import ReciboPagamento


class ListReciboPagamentoView(ListView, FinanceiroMixin):
    template_name = 'recibos/index.html'
    model = ReciboPagamento
    paginate_by = 5
    ordering = ('id',)

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        queryset = self.model.objects.filter(
            Q(nome__startswith=termo_pesquisa)
        )

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


class CriarReciboPagamentoView(CreateView, FinanceiroProtegidoMixin):
    template_name = "recibos/form.html"
    model = ReciboPagamento
    success_url = reverse_lazy('financeiro-recibos')
    permission_required = 'financeiro.add_recibopagamento'
    fields = ('nome',)


class EditarReciboPagamentoView(UpdateView, FinanceiroProtegidoMixin):
    template_name = "recibos/form.html"
    model = ReciboPagamento
    success_url = reverse_lazy('financeiro-recibos')
    permission_required = 'financeiro.change_recibopagamento'
    fields = ('nome',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Editar"
        return context


class RemoverReciboPagamentoView(DeleteView, FinanceiroProtegidoMixin):
    model = ReciboPagamento
    success_url = reverse_lazy('financeiro-recibos')
    permission_required = 'financeiro.delete_recibopagamento'

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return self.post(request, *args, **kwargs)


class VerReciboPagamentoView(DetailView, FinanceiroProtegidoMixin):
    template_name = "recibos/ver.html"
    model = ReciboPagamento
    permission_required = 'financeiro.view_recibopagamento'
