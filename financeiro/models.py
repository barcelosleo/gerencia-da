from django.db import models

class Carteira(models.Model):
    nome = models.CharField(max_length=50)

class EntradaFinanceira(models.Model):
    valor = models.FloatField()
    carteira = models.ForeignKey(Carteira, on_delete=models.PROTECT)
    data = models.DateField(auto_now=True)

class SaidaFinanceira(models.Model):
    valor = models.FloatField()
    data = models.DateField(auto_now=True)
    carteira = models.ForeignKey(Carteira, on_delete=models.PROTECT)

class TransferenciaFinanceira(models.Model):
    valor = models.FloatField()
    data = models.DateField(auto_now=True)
    carteira_origem = models.ForeignKey(Carteira, related_name='transferencias_de', on_delete=models.PROTECT)
    carteira_destino = models.ForeignKey(Carteira, related_name='transferencias_para', on_delete=models.PROTECT)

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.FloatField()
    servico = models.BooleanField(default=False)
    arquivado = models.BooleanField(default=False)
    foto = models.FileField(null=True)

class Venda(models.Model):
    desconto = models.IntegerField(default=0)
    associado = models.ForeignKey("gestao.Associado", on_delete=models.PROTECT, null=True)
    entrada_financeira = models.ForeignKey(EntradaFinanceira, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through="VendaProduto")

class VendaProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    desconto = models.IntegerField(default=0)

class ReciboVenda(models.Model):
    data = models.DateField(auto_now=True)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    associado = models.ForeignKey("gestao.Associado", on_delete=models.CASCADE)