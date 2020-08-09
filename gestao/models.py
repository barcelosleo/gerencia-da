from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from gestao import managers
from datetime import timedelta
import uuid


def diretorio_usuario(instancia, arquivo):
    return f"images/aluno_{instancia.matricula}/{arquivo}"


def mais_h():
    return timezone.now() + timedelta(hours=24)


class Associado(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=60)
    ano_matricula = models.IntegerField(null=True, verbose_name="Ano de Matrícula", blank=True)
    previsao_conclusao = models.IntegerField(null=True, verbose_name="Previsão de Conclusão", blank=True)
    telefone = models.CharField(max_length=30, null=True, blank=True)
    matricula = models.CharField(max_length=30, unique=True, verbose_name="Matrícula")
    foto = models.ImageField(upload_to=diretorio_usuario, blank=True, null=True)
    usuario_externo = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False, verbose_name="É diretor?",
                                   help_text="O associado faz parte da chapa eleita?")
    is_active = models.BooleanField(default=True, verbose_name="Aluno Ativo?",
                                    help_text="O associado ainda está estudado?")
    is_external = models.BooleanField(default=False, verbose_name="Usuário Externo?",
                                      help_text="Este usuário não é um associado do Diretório Acadêmico?")
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'matricula'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email']

    objects = managers.AssociadoManager()

    @property
    def nome_completo(self):
        return f"{self.nome} {self.sobrenome}"

    def __str__(self):
        return f"{self.matricula} - {self.nome_completo}"

    class Meta:
        verbose_name = "Associado"
        verbose_name_plural = "Associados"


class Aluno(Associado):
    objects = managers.AlunoManager()

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        proxy = True


class Diretor(Associado):
    objects = managers.DiretorManager()

    class Meta:
        verbose_name = "Diretor"
        verbose_name_plural = "Diretores"
        proxy = True


class Egresso(Associado):
    objects = managers.EgressoManager()

    class Meta:
        verbose_name = "Egresso"
        verbose_name_plural = "Egressos"
        proxy = True


class Externo(Associado):
    objects = managers.ExternoManager()

    class Meta:
        verbose_name = "Usuário Externo"
        verbose_name_plural = "Usuários Externos"
        proxy = True


class Area(models.Model):
    nome = models.CharField(max_length=50)
    gestor = models.ForeignKey(Associado, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Area"
        verbose_name_plural = "Areas"


class Reuniao(models.Model):
    data = models.DateField(default=timezone.now, verbose_name="Data da reunião")
    titulo = models.CharField(max_length=50, verbose_name="Título da Ata", null=True)
    ata = models.TextField(verbose_name="Transcrição da ata...")
    presentes = models.ManyToManyField(Associado, related_name='reunioes', blank=True)

    class Meta:
        verbose_name = "Reunião"
        verbose_name_plural = "Reuniões"


class DiretorioAcademico(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do diretório acadêmico")
    sigla = models.CharField(max_length=10, verbose_name="Sigla do diretório acadêmico", default="")
    logo = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Logo do diretório")

    class Meta:
        verbose_name = "Diretorio Acadêmico"
        verbose_name_plural = "Diretorio Acadêmico"


class LinkCadastro(models.Model):
    class TipoUsuario(models.IntegerChoices):
        DIRETOR = 1, 'Diretor'
        ALUNO = 2, 'Aluno'
        EGRESSO = 3, 'Egresso'
        EXTERNO = 4, 'Usuário Externo'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usado = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True)
    validade = models.DateTimeField(default=mais_h)
    tipo_usuario = models.PositiveIntegerField(choices=TipoUsuario.choices)
    reutilizavel = models.BooleanField(default=False)
