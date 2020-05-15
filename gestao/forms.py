from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db.models import Q
from django.contrib.auth.models import Group
import material

from gestao import models

class ModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nome}"

class MultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nome}"

class AssociadoCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = models.Associado
        fields = ('matricula', 'email',)

class AssociadoChangeForm(UserChangeForm):
    class Meta:
        model = models.Associado
        fields = ('matricula', 'email',)

class DiretorioAcademicoForm(forms.ModelForm):
    class Meta:
        model = models.DiretorioAcademico
        fields = ("nome", "sigla", "logo", )

class AreaForm(forms.ModelForm):
    gestor = ModelChoiceField(queryset=models.Associado.objects.filter(Q(is_staff=True) & Q(is_active=True)), empty_label="Sem Gestor", required=False)
    class Meta:
        model = models.Area
        fields = ("nome",)

class DiretorCargoForm(forms.ModelForm):
    class Meta:
        model = models.Diretor
        fields = ("groups", )

class AssociadoForm(forms.ModelForm):
    layout = material.Layout(
        material.Fieldset("Informações Pessoais",
            material.Row('nome', 'sobrenome'),
            material.Row('email', 'telefone'),
        ),
        material.Fieldset("Informações de Curso",
            material.Row('matricula', 'ano_matricula', 'previsao_conclusao', 'is_active')
        ),
        material.Fieldset("Informações de Permissão",
            material.Row('is_staff')
        ),
    )

    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'mascara-telefone'}), required=False)

    class Meta:
        model = models.Associado
        fields = (
            "nome",
            "sobrenome",
            "matricula",
            "email",
            "ano_matricula",
            "previsao_conclusao",
            "telefone",
            "is_staff",
            "is_active"
        )

class EgressoForm(forms.ModelForm):
    layout = material.Layout(
        material.Fieldset("Informações Pessoais",
            material.Row('nome', 'sobrenome'),
            material.Row('email', 'telefone'),
        ),
        material.Fieldset("Informações de Curso",
            material.Row('ano_matricula', 'previsao_conclusao')
        ),
    )

    previsao_conclusao = forms.IntegerField(label="Ano de Conclusão", required=False)
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'mascara-telefone'}), required=False)

    class Meta:
        model = models.Egresso
        fields = (
            "nome",
            "sobrenome",
            "email",
            "ano_matricula",
            "previsao_conclusao",
            "telefone",
        )

class ReuniaoForm(forms.ModelForm):
    ata = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'editor'}))
    data = forms.DateField(label="Data da Reunião", widget=forms.DateInput(format='%d/%m/%Y'), input_formats=('%d/%m/%Y', ))
    presentes = MultipleModelChoiceField(queryset=models.Associado.objects.filter(is_active=True))

    class Meta:
        model = models.Reuniao
        fields = ("data", "titulo", "ata", "presentes")

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name", "permissions", )
