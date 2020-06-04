from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid

def mais_d():
    return timezone.now() + timedelta(days=7)

class Carteira(models.Model):
    nome = models.CharField(max_length=50)

    @property
    def saldo(self):
        """Saldo efetivo da carteira financeira"""
        entradas = EntradaFinanceira.objects.filter(
            carteira=self,
            efetivado=True
        ).aggregate(total=models.Sum('valor'))

        saidas = SaidaFinanceira.objects.filter(
            carteira=self,
            efetivado=True
        ).aggregate(total=models.Sum('valor'))

        transferencias_para = TransferenciaFinanceira.objects.filter(
            carteira_destino=self,
            efetivado=True
        ).aggregate(total=models.Sum('valor'))

        transferencias_de = TransferenciaFinanceira.objects.filter(
            carteira_origem=self,
            efetivado=True
        ).aggregate(total=models.Sum('valor'))

        saldo = 0.0

        if entradas['total']:
            saldo += entradas['total']

        if transferencias_para['total']:
            saldo += transferencias_para['total']

        if saidas['total']:
            saldo -= saidas['total']

        if transferencias_de['total']:
            saldo -= transferencias_de['total']

        return saldo

    def __str__(self):
        return self.nome


class EntradaFinanceira(models.Model):
    valor = models.FloatField()
    carteira = models.ForeignKey(Carteira, on_delete=models.PROTECT)
    descricao = models.CharField(max_length=100)
    data = models.DateField(default=timezone.now)
    efetivado = models.BooleanField(default=False)

class SaidaFinanceira(models.Model):
    valor = models.FloatField()
    carteira = models.ForeignKey(Carteira, on_delete=models.PROTECT)
    descricao = models.CharField(max_length=100)
    data = models.DateField(default=timezone.now)
    efetivado = models.BooleanField(default=False)

class TransferenciaFinanceira(models.Model):
    valor = models.FloatField()
    descricao = models.CharField(max_length=100)
    data = models.DateField(default=timezone.now)
    efetivado = models.BooleanField(default=False)
    carteira_origem = models.ForeignKey(
        Carteira,
        related_name='transferencias_de',
        on_delete=models.PROTECT
    )
    carteira_destino = models.ForeignKey(
        Carteira,
        related_name='transferencias_para',
        on_delete=models.PROTECT
    )

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.FloatField()
    servico = models.BooleanField(default=False)
    arquivado = models.BooleanField(default=False)
    foto = models.ImageField(upload_to='images/produtos/', null=True, blank=True)

    def __str__(self):
        preco = '{:,.2f}'.format(self.preco)
        preco = preco.replace(',', 'v')
        preco = preco.replace('.', ',')
        preco = preco.replace('v', '.')
        return f"R$ {preco} - {self.nome}"

class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE, primary_key=True)
    quantidade = models.PositiveIntegerField()
    quantidade_minima = models.PositiveIntegerField(default=0)
    quantidade_encomenda = models.PositiveIntegerField()

class Venda(models.Model):
    associado = models.ForeignKey("gestao.Associado", on_delete=models.PROTECT, null=True)
    data = models.DateField(default=timezone.now)
    desconto = models.FloatField(default=0)
    finalizada = models.BooleanField(default=False)
    codigo = models.UUIDField(default=uuid.uuid4)
    entradas = models.ManyToManyField(EntradaFinanceira, through="VendaEntrada")
    produtos = models.ManyToManyField(Produto, through="VendaProduto")

    @property
    def total(self):
        total = 0
        for venda_produto in self.venda_produtos.all():
            total += venda_produto.produto.preco * venda_produto.quantidade

        return total

    @property
    def venda_produtos(self):
        return VendaProduto.objects.filter(venda=self)

    @property
    def cobranca(self):
        return self.total - self.desconto

class VendaProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    @property
    def total(self):
        return self.produto.preco * self.quantidade

class VendaEntrada(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    entrada = models.ForeignKey(EntradaFinanceira, on_delete=models.CASCADE)

class ReciboPagamento(models.Model):
    data = models.DateField(auto_now=True)
    entrada = models.ForeignKey(EntradaFinanceira, on_delete=models.CASCADE)
    associado = models.ForeignKey("gestao.Associado", on_delete=models.CASCADE)

class TemporadaEncomenda(models.Model):
    data = models.DateField(auto_now=True)
    data_fim = models.DateField(default=mais_d)
    produtos = models.ManyToManyField(Produto, related_name="temporadas_encomenda")
    ativa = models.BooleanField(default=True)

class Encomenda(models.Model):
    data = models.DateTimeField(auto_now=True)
    associado = models.ForeignKey("gestao.Associado", on_delete=models.CASCADE)
    temporada_encomenda = models.ForeignKey(TemporadaEncomenda, on_delete=models.PROTECT)
    total = models.FloatField(default=0)
    produtos = models.ManyToManyField(Produto, through="EncomendaProduto")

class EncomendaProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    encomenda = models.ForeignKey(Encomenda, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    total = models.FloatField(default=0)
