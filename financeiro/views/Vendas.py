from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView

from financeiro.mixins import FinanceiroMixin, FinanceiroProtegidoMixin

from financeiro.models import Venda, VendaProduto, VendaEntrada, EntradaFinanceira
from financeiro.forms import VendaForm, VendaProdutoForm, VendaEntradaForm, VendaEntradaInlineFormset, VendaProdutoInlineFormset


class ListVendaView(ListView, FinanceiroMixin):
    template_name = 'vendas/index.html'
    model = Venda
    paginate_by = 5
    ordering = ('id',)

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('termo', '')
        queryset = self.model.objects.filter(
            Q(associado__nome__startswith=termo_pesquisa)
        )

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


class CriarVendaView(CreateView, FinanceiroProtegidoMixin):
    template_name = "vendas/form.html"
    model = Venda
    success_url = reverse_lazy('financeiro-vendas')
    permission_required = 'financeiro.add_venda'
    form_class = VendaForm
    produto_formset = inlineformset_factory(
        Venda,
        VendaProduto,
        form=VendaProdutoForm,
        formset=VendaProdutoInlineFormset,
        extra=0,
        can_delete=False,
        min_num=1,
        max_num=20,
    )

    def get_context_data(self, **kwargs):
        context = super(CriarVendaView, self).get_context_data()
        context['venda_produto_formset'] = self.produto_formset
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_venda = self.get_form()
        formset_produtos = self.produto_formset(request.POST)

        if form_venda.is_valid() and formset_produtos.is_valid():
            venda = form_venda.save()
            self.object = venda
            formset_produtos.instance = venda
            formset_produtos.save()

            return redirect('financeiro-vendas-parcelas', pk=self.object.id)

        context = self.get_context_data(form=form_venda)
        context['venda_produto_formset'] = formset_produtos

        return self.render_to_response(context)


class EditarVendaView(UpdateView, FinanceiroProtegidoMixin):
    template_name = "vendas/form.html"
    model = Venda
    success_url = reverse_lazy('financeiro-vendas')
    permission_required = 'financeiro.change_venda'
    form_class = VendaForm
    produto_formset = inlineformset_factory(
        Venda,
        VendaProduto,
        form=VendaProdutoForm,
        extra=0,
        can_delete=True,
        min_num=1,
        max_num=20,
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Editar"
        context['venda_produto_formset'] = self.produto_formset(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_venda = self.get_form()
        formset_produtos = self.produto_formset(request.POST, instance=self.object)

        if self.object.finalizada:
            return redirect('financeiro-vendas-parcelas', pk=self.object.id)

        if self.object.entradas.count() > 0:
            form_venda.save()
            return redirect('financeiro-vendas-parcelas', pk=self.object.id)

        if form_venda.is_valid() and formset_produtos.is_valid():
            form_venda.save()
            formset_produtos.save()

            return redirect('financeiro-vendas-parcelas', pk=self.object.id)

        context = self.get_context_data(form=form_venda)
        context['venda_produto_formset'] = formset_produtos

        return self.render_to_response(context)


class RemoverVendaView(DeleteView, FinanceiroProtegidoMixin):
    model = Venda
    success_url = reverse_lazy('financeiro-vendas')
    permission_required = 'financeiro.delete_venda'

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        parcelas = self.object.entradas.all()

        for parcela in parcelas:
            parcela.delete()

        success_url = self.get_success_url()

        self.object.delete()

        return HttpResponseRedirect(success_url)


class VerVendaView(DetailView, FinanceiroProtegidoMixin):
    template_name = "vendas/ver.html"
    model = Venda
    permission_required = 'financeiro.view_venda'


class ParcelasVenda(FormView, FinanceiroProtegidoMixin):
    template_name = "vendas/parcelas.html"
    model = Venda
    form_class = inlineformset_factory(
        Venda,
        VendaEntrada,
        form=VendaEntradaForm,
        extra=0,
        can_delete=False,
        min_num=1,
        max_num=10,
        formset=VendaEntradaInlineFormset
    )
    permission_required = 'financeiro.change_venda'
    success_url = reverse_lazy('financeiro-vendas')

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST, instance=self.get_object())

        if forms.is_valid():
            return self.form_valid(forms)

        context = self.get_context_data()

        for form in forms:
            # Gambizinha para que os valores dos campos disabled "voltem"
            if form.instance.entrada.efetivado:
                form.fields['data'].widget.attrs['value'] = form.fields['data'].initial.strftime('%d/%m/%Y')
                form.fields['valor'].widget.attrs['value'] = form.fields['valor'].initial
                form.fields['carteira'].choices = [
                    form.fields['carteira'].choices.choice(form.cleaned_data['carteira'])
                ]
                form.fields['efetivado'].widget.attrs['checked'] = 'checked'

        context['form'] = forms

        return self.render_to_response(context)

    def form_valid(self, forms):
        venda = self.get_object()

        finalizada = True

        i = 1
        n_parcelas = len(forms)

        decrementar_estoque = False

        for form in forms:
            parcela = form.save(commit=False)

            finalizada &= form.cleaned_data.get('efetivado')

            if form.cleaned_data['id']:
                parcela = form.cleaned_data['id']
                entrada = parcela.entrada
                if not entrada.efetivado:
                    entrada.data = form.cleaned_data.get('data')
                    entrada.efetivado = form.cleaned_data.get('efetivado')
                    entrada.valor = form.cleaned_data.get('valor')
                    entrada.carteira = form.cleaned_data.get('carteira')
                    entrada.save()

            else:
                decrementar_estoque = True
                entrada = EntradaFinanceira.objects.create(
                    valor=form.cleaned_data.get('valor'),
                    carteira=form.cleaned_data.get('carteira'),
                    descricao=f"Venda({parcela.venda.codigo}) - Parcela {i} de {n_parcelas}",
                    data=form.cleaned_data.get('data'),
                    efetivado=form.cleaned_data.get('efetivado')
                )
                entrada.save()
                parcela.entrada = entrada

            parcela.save()

            i += 1

        if finalizada:
            venda.finalizada = True
            venda.save()

        # Caso as parcelas estejam sendo criadas, o estoque é decrementado visto que não é mais possível alterar a venda
        if decrementar_estoque:
            for venda_produto in venda.venda_produtos.filter(produto__servico=False):
                venda_produto.produto.estoque.quantidade -= venda_produto.quantidade
                venda_produto.produto.estoque.save()

        return redirect('financeiro-vendas')

    def get_object(self):
        return Venda.objects.get(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        venda = self.get_object()
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(instance=venda)
        context["venda"] = venda
        return context
