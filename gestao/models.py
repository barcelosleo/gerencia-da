from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import AssociadoManager
from django.dispatch import receiver
import os

def diretorio_usuario(instancia, arquivo):
    return f"images/aluno_{instancia.matricula}/{arquivo}"

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
    is_staff = models.BooleanField(default=False, verbose_name="É diretor?", help_text="O associado faz parte da chapa eleita?")
    is_active = models.BooleanField(default=True, verbose_name="Aluno Ativo?", help_text="O associado ainda está estudado?")
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'matricula'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email']

    objects = AssociadoManager()

class Area(models.Model):
    nome = models.CharField(max_length=50)
    gestor = models.ForeignKey(Associado, on_delete=models.SET_NULL, null=True, blank=True)

class Cargo(models.Model):
    nome = models.CharField(max_length=30)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    associados = models.ManyToManyField(Associado, related_name="cargos")

class Reuniao(models.Model):
    data = models.DateField(auto_now=True, verbose_name="Data da reunião")
    ata = models.TextField(verbose_name="Transcrição da ata...")
    presentes = models.ManyToManyField(Associado)

class DiretorioAcademico(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do diretório acadêmico")
    sigla = models.CharField(max_length=10, verbose_name="Sigla do diretório acadêmico", default="")
    logo = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Logo do diretório")

@receiver(models.signals.pre_save, sender=DiretorioAcademico)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).logo
    except sender.DoesNotExist:
        return False

    new_file = instance.logo
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

@receiver(models.signals.pre_save, sender=Associado)
def auto_delete_file_on_change_associado(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).foto
    except sender.DoesNotExist:
        return False

    new_file = instance.foto
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

@receiver(models.signals.post_delete, sender=Associado)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.foto:
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)

