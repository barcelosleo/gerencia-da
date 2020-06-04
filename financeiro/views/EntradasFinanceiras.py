from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from financeiro.mixins import FinanceiroMixin, FinanceiroProtegidoMixin

from financeiro.models import EntradaFinanceira
from financeiro.forms import EntradaFinanceiraForm

class ListEntradaFinanceiraView(ListView, FinanceiroMixin):
    template_name = 'entradas/index.html'
    model = EntradaFinanceira
    paginate_by = 5
    ordering = ('id', )

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        queryset = self.model.objects.filter(
            Q(descricao__startswith=termo_pesquisa)
        )

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

class CriarEntradaFinanceiraView(CreateView, FinanceiroProtegidoMixin):
    template_name = "entradas/form.html"
    model = EntradaFinanceira
    success_url = reverse_lazy('financeiro-entradas')
    permission_required = 'financeiro.add_entradafinanceira'
    form_class = EntradaFinanceiraForm

class EditarEntradaFinanceiraView(UpdateView, FinanceiroProtegidoMixin):
    template_name = "entradas/form.html"
    model = EntradaFinanceira
    success_url = reverse_lazy('financeiro-entradas')
    permission_required = 'financeiro.change_entradafinanceira'
    form_class = EntradaFinanceiraForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Editar"
        return context


class RemoverEntradaFinanceiraView(DeleteView, FinanceiroProtegidoMixin):
    model = EntradaFinanceira
    success_url = reverse_lazy('financeiro-entradas')
    permission_required = 'financeiro.delete_entradafinanceira'

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return self.post(request, *args, **kwargs)

class VerEntradaFinanceiraView(DetailView, FinanceiroProtegidoMixin):
    template_name = "entradas/ver.html"
    model = EntradaFinanceira
    permission_required = 'financeiro.view_entradafinanceira'