from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from financeiro.mixins import FinanceiroMixin, FinanceiroProtegidoMixin

from financeiro.models import Carteira

class ListCarteiraView(ListView, FinanceiroMixin):
    template_name = 'carteiras/index.html'
    model = Carteira
    paginate_by = 5
    ordering = ('id', )

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

class CriarCarteiraView(CreateView, FinanceiroProtegidoMixin):
    template_name = "carteiras/form.html"
    model = Carteira
    success_url = reverse_lazy('financeiro-carteiras')
    permission_required = 'financeiro.add_carteira'
    fields = ('nome', )

class EditarCarteiraView(UpdateView, FinanceiroProtegidoMixin):
    template_name = "carteiras/form.html"
    model = Carteira
    success_url = reverse_lazy('financeiro-carteiras')
    permission_required = 'financeiro.change_carteira'
    fields = ('nome', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Editar"
        return context


class RemoverCarteiraView(DeleteView, FinanceiroProtegidoMixin):
    model = Carteira
    success_url = reverse_lazy('financeiro-carteiras')
    permission_required = 'financeiro.delete_carteira'

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return self.post(request, *args, **kwargs)

class VerCarteiraView(DetailView, FinanceiroProtegidoMixin):
    template_name = "carteiras/ver.html"
    model = Carteira
    permission_required = 'financeiro.view_carteira'
