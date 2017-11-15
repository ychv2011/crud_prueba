from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from todo.views import Login, ListadoNotas, CrearNota, Registro, DetalleNota, EliminarNota, ModificarNota, Cuenta

urlpatterns = [
    url(r'^$', ListadoNotas.as_view(), name="notas"),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^registro/$', Registro.as_view(), name='registro'),
    url(r'^cuenta/$', login_required(Cuenta.as_view()), name='cuenta'),
    url(r'^crear-nota/$', login_required(CrearNota.as_view()), name="crear_nota"),
    url(r'^detalle-nota/(?P<pk>\d+)/$', DetalleNota.as_view(), name="detalle_nota"),
    url(r'^modificar-nota/(?P<pk>\d+)/$', login_required(ModificarNota.as_view()), name="modificar_nota"),
    url(r'^eliminar-nota/(?P<pk>\d+)/$', login_required(EliminarNota.as_view()), name="eliminar_nota"),
    url(r'^salir$', logout, name="salir", kwargs={'next_page': 'todo:notas'}),
]