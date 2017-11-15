from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, TemplateView, FormView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth import login, authenticate, logout
from todo.forms import NotaForm, FormularioLogin, RegistroForm, CuentaForm
from todo.models import Nota

class Registro(FormView):
    template_name = 'registro.html'
    form_class = RegistroForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return redirect("todo:notas")

class Cuenta(FormView):
    template_name = 'cuenta.html'
    form_class = CuentaForm
    success_url = reverse_lazy("todo:notas")

    def get_initial(self):
        initial = super(Cuenta, self).get_initial()
        initial['username'] = self.request.user
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        return initial

    def get_form_kwargs(self):
        kwargs = super(Cuenta, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        print(form)
        return self.render_to_response(self.get_context_data(form=form))

class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy("todo:notas")

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

class ListadoNotas(ListView):
    template_name = 'notas.html'
    model = Nota
    context_object_name = 'notas'

    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_authenticated():
            queryset = Nota.objects.filter(Q(usuario=usuario) | Q(publico=True))
        else:
            queryset = Nota.objects.filter(publico=True)
        return queryset


class CrearNota(CreateView):
    template_name = 'nota.html'
    model = Nota
    form_class = NotaForm
    success_url = reverse_lazy("todo:notas")

    def get_form_kwargs(self):
        kwargs = super(CrearNota, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class DetalleNota(DetailView):
    template_name = 'detalle_nota.html'
    model = Nota

class ModificarNota(UpdateView):
    model = Nota
    template_name = 'nota.html'
    form_class = NotaForm

    def get_form_kwargs(self):
        kwargs = super(ModificarNota, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse('todo:notas')

class EliminarNota(DeleteView):
    model = Nota
    template_name = 'eliminar_nota.html'

    def get_success_url(self):
        return reverse('todo:notas')