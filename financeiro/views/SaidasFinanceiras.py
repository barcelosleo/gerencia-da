from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from financeiro.mixins import FinanceiroMixin, FinanceiroProtegidoMixin

from financeiro.models import SaidaFinanceira
from financeiro.forms import SaidaFinanceiraForm

class ListSaidaFinanceiraView(ListView, FinanceiroMixin):
    template_name = 'saidas/index.html'
    model = SaidaFinanceira
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

class CriarSaidaFinanceiraView(CreateView, FinanceiroProtegidoMixin):
    template_name = "saidas/form.html"
    model = SaidaFinanceira
    success_url = reverse_lazy('financeiro-saidas')
    permission_required = 'financeiro.add_saidafinanceira'
    form_class = SaidaFinanceiraForm

class EditarSaidaFinanceiraView(UpdateView, FinanceiroProtegidoMixin):
    template_name = "saidas/form.html"
    model = SaidaFinanceira
    success_url = reverse_lazy('financeiro-saidas')
    permission_required = 'financeiro.change_saidafinanceira'
    form_class = SaidaFinanceiraForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Editar"
        return context


class RemoverSaidaFinanceiraView(DeleteView, FinanceiroProtegidoMixin):
    model = SaidaFinanceira
    success_url = reverse_lazy('financeiro-saidas')
    permission_required = 'financeiro.delete_saidafinanceira'

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return self.post(request, *args, **kwargs)

class VerSaidaFinanceiraView(DetailView, FinanceiroProtegidoMixin):
    template_name = "saidas/ver.html"
    model = SaidaFinanceira
    permission_required = 'financeiro.view_saidafinanceira'