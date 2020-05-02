from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import Associado, DiretorioAcademico, Area, Cargo

class ModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nome}"

class MultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nome}"

class AssociadoCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Associado
        fields = ('matricula', 'email',)


class AssociadoChangeForm(UserChangeForm):

    class Meta:
        model = Associado
        fields = ('matricula', 'email',)

class DiretorioAcademicoForm(forms.ModelForm):
    class Meta:
        model = DiretorioAcademico
        fields = ("nome", "sigla", "logo", )

class AreaForm(forms.ModelForm):

    gestor = ModelChoiceField(queryset=Associado.objects.filter(is_staff=True), empty_label="Sem Gestor", required=False)
    class Meta:
        model = Area
        fields = ("nome",)

class CargoForm(forms.ModelForm):
    associados = MultipleModelChoiceField(queryset=Associado.objects.filter(is_staff=True), required=False)
    area = ModelChoiceField(queryset=Area.objects.all())

    class Meta:
        model = Cargo
        fields = ("nome", "area", "associados", )

class DiretorCargoForm(forms.ModelForm):
    cargos = MultipleModelChoiceField(queryset=Cargo.objects.all(), required=False)

    class Meta:
        model = Associado
        fields = ("cargos", )

class AssociadoForm(forms.ModelForm):
    class Meta:
        model = Associado
        fields = ("nome", "sobrenome", "matricula", "email", "ano_matricula", "previsao_conclusao", "telefone", "foto", "is_staff")