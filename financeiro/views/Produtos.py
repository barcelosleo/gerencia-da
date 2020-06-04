from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from financeiro.mixins import FinanceiroMixin, FinanceiroProtegidoMixin
from financeiro.models import Produto, Estoque
from financeiro.forms import ProdutoForm, EstoqueForm

class ListProdutoView(ListView, FinanceiroMixin):
    template_name = 'produtos/index.html'
    model = Produto
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

class CriarProdutoView(CreateView, FinanceiroProtegidoMixin):
    template_name = "produtos/form.html"
    model = Produto
    success_url = reverse_lazy('financeiro-produtos')
    permission_required = 'financeiro.add_produto'
    form_class = ProdutoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estoque_form"] = EstoqueForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        produto_form = ProdutoForm(request.POST)
        estoque_form = EstoqueForm(request.POST)

        produto_form.is_valid()

        if produto_form.cleaned_data['servico']:
            if produto_form.is_valid():
                return self.form_valid(produto_form)

            return self.form_invalid(produto_form)

        if produto_form.is_valid() and estoque_form.is_valid():
            produto = produto_form.save()

            estoque = estoque_form.save(commit=False)
            estoque.produto = produto
            estoque.save()

            return HttpResponseRedirect(self.success_url)

        context = self.get_context_data()
        context['estoque_form'] = estoque_form

        return self.render_to_response(context)

class EditarProdutoView(UpdateView, FinanceiroProtegidoMixin):
    template_name = "produtos/form.html"
    model = Produto
    success_url = reverse_lazy('financeiro-produtos')
    permission_required = 'financeiro.change_produto'
    form_class = ProdutoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto = self.get_object()
        context["action"] = "Editar"

        if produto.servico:
            context["estoque_form"] = EstoqueForm()
            return context

        context["estoque_form"] = EstoqueForm(instance=produto.estoque)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        produto_form = ProdutoForm(request.POST, instance=self.object)

        produto_form.is_valid()

        if produto_form.cleaned_data['servico']:
            if produto_form.is_valid():
                try:
                    self.object.estoque.delete()
                except ObjectDoesNotExist:
                    pass

                return self.form_valid(produto_form)

            return self.form_invalid(produto_form)

        try:
            estoque_form = EstoqueForm(request.POST, instance=self.object.estoque)
        except ObjectDoesNotExist:
            estoque_form = EstoqueForm(request.POST)


        if produto_form.is_valid() and estoque_form.is_valid():
            produto = produto_form.save()

            estoque = estoque_form.save(commit=False)
            estoque.produto = produto
            estoque.save()

            return HttpResponseRedirect(self.success_url)

        context = self.get_context_data()
        context['estoque_form'] = estoque_form

        return self.render_to_response(context)


class RemoverProdutoView(DeleteView, FinanceiroProtegidoMixin):
    model = Produto
    success_url = reverse_lazy('financeiro-produtos')
    permission_required = 'financeiro.delete_produto'

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return self.post(request, *args, **kwargs)

class VerProdutoView(DetailView, FinanceiroProtegidoMixin):
    template_name = "produtos/ver.html"
    model = Produto
    permission_required = 'financeiro.view_produto'