from django import forms
import material

from gestao import models

class AlunoForm(forms.ModelForm):
    layout = material.Layout(
        material.Fieldset("Informações Pessoais",
            material.Row('nome', 'sobrenome'),
            material.Row('email', 'telefone'),
        ),
        material.Fieldset("Informações de Curso",
            material.Row('matricula', 'ano_matricula', 'previsao_conclusao')
        ),
        material.Fieldset("Informações de Acesso",
            material.Row('password', 'password_confirm')
        ),
    )
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())
    password_confirm = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput())
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'mascara-telefone'}), required=False)


    def clean(self):
        cleaned_data = super(AlunoForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError(
                "password and password_confirm does not match"
            )

    class Meta:
        model = models.Aluno
        fields = (
            "nome",
            "sobrenome",
            "matricula",
            "email",
            "ano_matricula",
            "previsao_conclusao",
            "telefone",
            "password",
        )

class DiretorForm(forms.ModelForm):
    layout = material.Layout(
        material.Fieldset("Informações Pessoais",
            material.Row('nome', 'sobrenome'),
            material.Row('email', 'telefone'),
        ),
        material.Fieldset("Informações de Curso",
            material.Row('matricula', 'ano_matricula', 'previsao_conclusao')
        ),
        material.Fieldset("Informações de Acesso",
            material.Row('password', 'password_confirm')
        ),
    )
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())
    password_confirm = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput())
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'mascara-telefone'}), required=False)


    def clean(self):
        cleaned_data = super(DiretorForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError(
                "password and password_confirm does not match"
            )

    class Meta:
        model = models.Diretor
        fields = (
            "nome",
            "sobrenome",
            "matricula",
            "email",
            "ano_matricula",
            "previsao_conclusao",
            "telefone",
            "password",
        )

class EgressoForm(forms.ModelForm):
    layout = material.Layout(
        material.Fieldset("Informações Pessoais",
            material.Row('nome', 'sobrenome'),
            material.Row('email', 'telefone'),
        ),
        material.Fieldset("Informações de Curso",
            material.Row('matricula', 'ano_matricula', 'previsao_conclusao')
        ),
        material.Fieldset("Informações de Acesso",
            material.Row('password', 'password_confirm')
        ),
    )
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())
    password_confirm = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput())
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'mascara-telefone'}), required=False)


    def clean(self):
        cleaned_data = super(EgressoForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError(
                "password and password_confirm does not match"
            )

    class Meta:
        model = models.Egresso
        fields = (
            "nome",
            "sobrenome",
            "matricula",
            "email",
            "ano_matricula",
            "previsao_conclusao",
            "telefone",
            "password",
        )
