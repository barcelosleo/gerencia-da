from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import Group
from gestao import models
import os


@receiver(signals.pre_save, sender=models.DiretorioAcademico)
def atualiza_foto_diretorio(sender, instance, **kwargs):
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

@receiver(signals.pre_save, sender=models.Associado)
def atualiza_foto_associado(sender, instance, **kwargs):
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

@receiver(signals.post_delete, sender=models.Associado)
def deleta_foto_associado(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.foto:
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)

@receiver(signals.post_save, sender=models.Diretor)
def grupo_padrao_diretor(sender, instance, **kwargs):
    grupo = Group.objects.get(pk=1)
    if instance.is_staff and not instance.is_external:
        instance.groups.add(grupo)
    else:
        instance.groups.remove(grupo)

@receiver(signals.post_save, sender=models.Aluno)
def grupo_padrao_aluno(sender, instance, **kwargs):
    grupo = Group.objects.get(pk=2)
    if not instance.is_staff and not instance.is_external:
        instance.groups.add(grupo)
    else:
        instance.groups.remove(grupo)

@receiver(signals.post_save, sender=models.Egresso)
def grupo_padrao_egresso(sender, instance, **kwargs):
    grupo = Group.objects.get(pk=3)
    if not instance.is_active and not instance.is_external:
        instance.groups.add(grupo)
    else:
        instance.groups.remove(grupo)

@receiver(signals.post_save, sender=models.Externo)
def grupo_padrao_usuario_externo(sender, instance, **kwargs):
    grupo = Group.objects.get(pk=4)
    if instance.is_external:
        instance.groups.add(grupo)
    else:
        instance.groups.remove(grupo)
