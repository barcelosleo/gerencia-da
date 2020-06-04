from django.db.models import Q
from django import forms
from django.utils import timezone
import material

from financeiro.models import (
        EntradaFinanceira,
        SaidaFinanceira,
        TransferenciaFinanceira,
        Carteira,
        Produto,
        Estoque,
        Venda,
        VendaProduto,
        VendaEntrada,
    )
from gestao.models import Associado

class EntradaFinanceiraForm(forms.ModelForm):
    descricao = forms.CharField(max_length=100, label="Descrição")
    carteira = forms.ModelChoiceField(queryset=Carteira.objects.all())
    valor = forms.CharField(widget=forms.TextInput(attrs={'class': 'mascara-dinheiro'}))
    efetivado = forms.BooleanField(label="Efetivada", help_text="Movimentação Financeira já foi efetivada?", required=False)

    layout = material.Layout(
        material.Row('descricao', 'valor'),
        material.Row('data', 'efetivado'),
        material.Row('carteira')
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')

        if instance:
            valor = '{:,.2f}'.format(float(instance.valor))
            valor = valor.replace(',', 'v')
            valor = valor.replace('.', ',')
            valor = f"R$ {valor}"

            if 'initial' in kwargs:
                kwargs['initial']['valor'] = valor

        super(EntradaFinanceiraForm, self).__init__(*args, **kwargs)


    def clean_valor(self):
        """Tira formatação de moeda"""
        data = self.cleaned_data.get("valor")
        data = data.replace('R$', '')
        data = data.replace('.', '')
        data = data.replace(',', '.')
        data = float(data)
        return data

    class Meta:
        model = EntradaFinanceira
        fields = ('descricao', 'valor', 'carteira', 'data', 'efetivado')

class SaidaFinanceiraForm(forms.ModelForm):
    descricao = forms.CharField(max_length=100, label="Descrição")
    carteira = forms.ModelChoiceField(queryset=Carteira.objects.all())
    valor = forms.CharField(widget=forms.TextInput(attrs={'class': 'mascara-dinheiro'}))
    efetivado = forms.BooleanField(label="Efetivada", help_text="Movimentação Financeira já foi efetivada?", required=False)

    layout = material.Layout(
        material.Row('descricao', 'valor'),
        material.Row('data', 'efetivado'),
        material.Row('carteira')
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')

        if instance:
            valor = '{:,.2f}'.format(float(instance.valor))
            valor = valor.replace(',', 'v')
            valor = valor.replace('.', ',')
            valor = f"R$ {valor}"

            if 'initial' in kwargs:
                kwargs['initial']['valor'] = valor

        super(SaidaFinanceiraForm, self).__init__(*args, **kwargs)


    def clean_valor(self):
        """Tira formatação de moeda"""
        data = self.cleaned_data.get("valor")
        data = data.replace('R$', '')
        data = data.replace('.', '')
        data = data.replace(',', '.')
        data = float(data)
        return data

    class Meta:
        model = SaidaFinanceira
        fields = ('descricao', 'valor', 'carteira', 'data', 'efetivado')

class TransferenciaFinanceiraForm(forms.ModelForm):
    descricao = forms.CharField(max_length=100, label="Descrição")
    carteira_origem = forms.ModelChoiceField(queryset=Carteira.objects.all())
    carteira_destino = forms.ModelChoiceField(queryset=Carteira.objects.all())
    valor = forms.CharField(widget=forms.TextInput(attrs={'class': 'mascara-dinheiro'}))
    efetivado = forms.BooleanField(label="Efetivada", help_text="Movimentação Financeira já foi efetivada?", required=False)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')

        if instance:
            valor = '{:,.2f}'.format(float(instance.valor))
            valor = valor.replace(',', 'v')
            valor = valor.replace('.', ',')
            valor = f"R$ {valor}"

            if 'initial' in kwargs:
                kwargs['initial']['valor'] = valor

        super(TransferenciaFinanceiraForm, self).__init__(*args, **kwargs)

    def clean_valor(self):
        """Tira formatação de moeda"""
        data = self.cleaned_data.get("valor")
        data = data.replace('R$', '')
        data = data.replace('.', '')
        data = data.replace(',', '.')
        data = float(data)
        return data

    def clean_carteira_destino(self):
        carteira_destino = self.cleaned_data.get("carteira_destino")
        carteira_origem = self.cleaned_data.get("carteira_origem")

        if carteira_destino == carteira_origem:
            raise forms.ValidationError('A Carteira Destino deve ser diferente da de Origem')

        return carteira_destino


    class Meta:
        model = TransferenciaFinanceira
        fields = ('descricao', 'valor', 'carteira_origem', 'carteira_destino', 'data', 'efetivado')

class EstoqueForm(forms.ModelForm):
    quantidade = forms.IntegerField(
        help_text="Quantidade em estoque"
    )
    quantidade_minima = forms.IntegerField(
        label="Quantidade Mínima",
        help_text="Quantidade mínima em estoque para realização de encomenda",
    )
    quantidade_encomenda = forms.IntegerField(
        label="Quantidade para Encomenda",
        help_text="Quantidade mínima de interessados para encomenda"
    )

    layout = material.Layout(
        material.Fieldset('Informações de Estoque',
            material.Row('quantidade', 'quantidade_minima', 'quantidade_encomenda')
        ),
    )

    class Meta:
        model = Estoque
        fields = ('quantidade', 'quantidade_minima', 'quantidade_encomenda')

class ProdutoForm(forms.ModelForm):
    preco = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'mascara-dinheiro'}),
        label="Preço do Produto"
    )
    servico = forms.BooleanField(
        label="Serviço",
        help_text="Este produto é uma prestação de serviço?",
        required=False
    )

    layout = material.Layout(
        material.Fieldset('Informações do Produto',
            material.Row('nome', 'preco', 'servico'),
            material.Row('foto')
        ),
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')

        if instance:
            preco = str(instance.preco)
            preco = '{:,.2f}'.format(float(instance.preco))
            preco = preco.replace(',', 'v')
            preco = preco.replace('.', ',')
            preco = f"R$ {preco}"

            if 'initial' in kwargs:
                kwargs['initial']['preco'] = preco

        super(ProdutoForm, self).__init__(*args, **kwargs)

    def clean_preco(self):
        """Tira formatação de moeda"""
        data = self.cleaned_data.get("preco")
        data = data.replace('R$', '')
        data = data.replace('.', '')
        data = data.replace(',', '.')
        data = float(data)
        return data

    class Meta:
        model = Produto
        fields = ('nome', 'preco', 'servico', 'foto')

class VendaForm(forms.ModelForm):
    associado = forms.ModelChoiceField(queryset=Associado.objects.all().order_by('nome', 'sobrenome', 'matricula'))
    finalizada = forms.BooleanField(help_text="Venda foi concluída?", required=False)
    desconto = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'mascara-dinheiro'}),
        required=False
    )

    layout = material.Layout(
        material.Row('associado'),
        material.Row('data', 'desconto', 'finalizada'),
    )

    def __init__(self, *args, **kwargs):
        super(VendaForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            desconto = '{:,.2f}'.format(float(self.instance.desconto))
            desconto = desconto.replace(',', 'v')
            desconto = desconto.replace('.', ',')
            desconto = f"R$ {desconto}"

            self.fields['desconto'].widget.attrs['value'] = desconto

            if self.instance.finalizada:

                self.fields['associado'].widget.attrs['disabled'] = True
                self.fields['data'].widget.attrs['disabled'] = True
                self.fields['finalizada'].widget.attrs['disabled'] = True
                self.fields['desconto'].widget.attrs['disabled'] = True

            if self.instance.entradas.count() > 0:
                self.fields['desconto'].widget.attrs['disabled'] = True

    def clean_desconto(self):
        """Tira formatação de moeda"""
        if self.instance and self.instance.pk:
            if self.instance.entradas.count() > 0:
                return self.instance.desconto

        desconto = self.cleaned_data.get("desconto")
        desconto = desconto.replace('R$', '')
        desconto = desconto.replace('.', '')
        desconto = desconto.replace(',', '.')
        desconto = float(desconto)
        return desconto

    class Meta:
        model = Venda
        fields = ('associado', 'data', 'finalizada', 'desconto')

class VendaProdutoForm(forms.ModelForm):
    produto = forms.ModelChoiceField(queryset=Produto.objects.filter(arquivado=False))
    quantidade = forms.IntegerField(
        min_value=1,
        widget=forms.TextInput(
            attrs={
                'class': 'quantidade-produto'
            }
        ),
        initial=1
    )
    adicionar = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'somar-produto'
            }
        )
    )
    remover = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'diminuir-produto'
            }
        )
    )
    layout = material.Layout(
        material.Row(
            material.Span5('produto'),
            material.Field('remover'),
            material.Span3('quantidade'),
            material.Field('adicionar'),
            material.Span2('DELETE')
        )
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        if not instance:
            self.layout = material.Layout(
                material.Row(
                    material.Span6('produto'),
                    material.Field('remover'),
                    material.Span4('quantidade'),
                    material.Field('adicionar'),
                )
            )

        super(VendaProdutoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = VendaProduto
        fields = ('produto', 'quantidade',)

class VendaEntradaForm(forms.ModelForm):
    carteira = forms.ModelChoiceField(queryset=Carteira.objects.all())
    valor = forms.CharField(widget=forms.TextInput(attrs={'class': 'mascara-dinheiro'}))
    efetivado = forms.BooleanField(label="Efetivada", help_text="Dinheiro já recebido?", required=False)
    data = forms.DateField(initial=timezone.now())

    layout = material.Layout(
        material.Row(
            material.Span3('data'),
            material.Span3('valor'),
            material.Span3('carteira'),
            material.Span3('efetivado'),
        )
    )

    def __init__(self, *args, **kwargs):
        super(VendaEntradaForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            valor = '{:,.2f}'.format(float(self.instance.entrada.valor))
            valor = valor.replace(',', 'v')
            valor = valor.replace('.', ',')
            valor = f"R$ {valor}"

            self.fields['carteira'].initial = self.instance.entrada.carteira
            self.fields['valor'].initial = valor
            self.fields['efetivado'].initial = self.instance.entrada.efetivado
            self.fields['data'].initial = self.instance.entrada.data

            if self.instance.entrada.efetivado:
                self.fields['carteira'].widget.attrs['disabled'] = True
                self.fields['carteira'].required = False

                self.fields['valor'].widget.attrs['disabled'] = True
                self.fields['valor'].required = False

                self.fields['efetivado'].widget.attrs['disabled'] = True
                self.fields['efetivado'].required = False

                self.fields['data'].widget.attrs['disabled'] = True
                self.fields['data'].required = False


    def clean_data(self):
        """Tira formatação de moeda"""
        if self.instance and self.instance.pk:
            if self.instance.entrada.efetivado:
                return self.instance.entrada.data

        return self.cleaned_data.get('data')

    def clean_carteira(self):
        """Tira formatação de moeda"""
        if self.instance and self.instance.pk:
            if self.instance.entrada.efetivado:
                return self.instance.entrada.carteira

        return self.cleaned_data.get('carteira')

    def clean_efetivado(self):
        """Tira formatação de moeda"""
        if self.instance and self.instance.pk:
            if self.instance.entrada.efetivado:
                return self.instance.entrada.efetivado

        return self.cleaned_data.get('efetivado')

    def clean_valor(self):
        """Tira formatação de moeda"""
        if self.instance and self.instance.pk:
            if self.instance.entrada.efetivado:
                return self.instance.entrada.valor

        valor = self.cleaned_data.get("valor")
        valor = valor.replace('R$', '')
        valor = valor.replace('.', '')
        valor = valor.replace(',', '.')
        valor = float(valor)
        return valor

    class Meta:
        model = VendaEntrada
        fields = ()

class VendaEntradaInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(VendaEntradaInlineFormset, self).clean()

        total = 0

        for form in self.forms:
            if not form.is_valid():
                return

            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                total += form.cleaned_data['valor']

        if self.instance.cobranca is not None and self.instance.cobranca != total:
            raise forms.ValidationError('A soma dos valores das parcelas deve coincidir com o total a cobrar!')

