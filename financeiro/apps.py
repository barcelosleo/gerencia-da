from django.apps import AppConfig
from django.db.models import signals
from django.dispatch import receiver
from financeiro.models import EntradaFinanceira, ReciboPagamento


class FinanceiroConfig(AppConfig):
    name = 'financeiro'

    def ready(self):
        @receiver(signals.post_save, sender=EntradaFinanceira)
        def gera_recibo_pagamento(sender, instance, **kwargs):
            """Método que gera o recibo de pagamento para o usuário"""
            if instance.efetivado and instance.e_venda:
                if instance.venda_entrada.venda.associado is not None and ReciboPagamento.objects.filter(entrada=instance).count() == 0:
                    ReciboPagamento.objects.create(
                        associado=instance.venda_entrada.venda.associado,
                        entrada=instance
                    )
