from django.db import models

class Evento(models.Model):
    data = models.DateField()
    titulo = models.CharField(max_length=100)
    valor_inscricao = models.FloatField(null=True)

class AtracaoEvento(models.Model):
    data_horario_inicio = models.DateTimeField()
    data_horario_fim = models.DateTimeField()
    apresentador = models.CharField(max_length=100, null=True)
    local = models.CharField(max_length=100, null=True)
    TIPO_ATRACAO = (
        ('Palestra', 'Palestra'),
        ('Oficina', 'Oficina'),
        ('Visita Técnica', 'Visita Técnica'),
    )
    tipo = models.CharField(max_length=30, choices=TIPO_ATRACAO)
    vagas = models.IntegerField(null=True)

class InscricaoEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    associado = models.ForeignKey("gestao.Associado", on_delete=models.CASCADE, null=True)
    confirmado = models.BooleanField(default=False)
    atracoes = models.ManyToManyField(AtracaoEvento, through="InscricaoAtracao")

class InscricaoAtracao(models.Model):
    inscricao_evento = models.ForeignKey(InscricaoEvento, on_delete=models.CASCADE)
    atracao_evento = models.ForeignKey(AtracaoEvento, on_delete=models.CASCADE)
    confirmado = models.BooleanField(default=False)