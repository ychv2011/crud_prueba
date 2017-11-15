# coding=utf-8
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core.exceptions import ValidationError

from todo.models import Nota

class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CuentaForm(forms.ModelForm):
    password_actual = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_nueva = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_verificacion = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(CuentaForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = 'readonly'
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_password_actual(self):
        if self.cleaned_data.get('password_actual') and not self.request.user.check_password(
                self.cleaned_data['password_actual']):
            raise ValidationError('La contraseña ingresada no es la actual.')
        return self.cleaned_data['password_actual']

    def clean_password_nueva(self):
        if self.cleaned_data.get('password_nueva') and not len(self.cleaned_data['password_nueva']) > 6:
            raise ValidationError('La nueva contraseña no cumple los requisitos de seguridad mínimos.')
        return self.cleaned_data['password_nueva']

    def clean_password_verificacion(self):
        if self.cleaned_data.get('password_nueva') and self.cleaned_data.get('password_verificacion') and \
                        self.cleaned_data['password_nueva'] != self.cleaned_data['password_verificacion']:
            raise ValidationError('Las contraseñas no coinciden')
        return self.cleaned_data['password_verificacion']

    def clean(self):
        usuario = self.request.user
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password_actual = self.cleaned_data.get('password_actual')
        password_nueva = self.cleaned_data.get('password_nueva')
        password_verificacion = self.cleaned_data.get('password_verificacion')
        if password_actual and password_nueva and password_verificacion:
            password_nueva = self.clean_password_nueva()
            usuario.set_password(password_nueva)
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.email = email
            usuario.save()
            logout(self.request)

class FormularioLogin(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

class NotaForm(forms.ModelForm):

    class Meta:
        model = Nota
        fields = ['titulo','contenido','publico']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(NotaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field != 'publico':
                self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, *args, **kwargs):
        usuario = self.request.user
        self.instance.usuario = usuario
        return super(NotaForm, self).save(*args, **kwargs)