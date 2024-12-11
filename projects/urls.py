from django.urls import path
from .views import *

urlpatterns=[
    path('ofertas/',OfertasView.as_view(),name='ofertas'),
    path('ofertas/<int:id>/', OfertasView.as_view(), name='ofertas_process'),
    path('pagos/', PagosView.as_view(), name='pagos'),
    path('pagos/<int:id>/', PagosView.as_view(), name='pagos_process'),
    path('permisos/', PermisosView.as_view(), name='permisos_list'),
    path('usuarios/', UsuariosView.as_view(), name='usuarios'),
    path('usuarios/<int:id>/', UsuariosView.as_view(), name='usuario_process'),
    path('accesos/', AccesosView.as_view(), name='accesos_list'),
    path('accesos/<int:id>', AccesosView.as_view(), name='accesos_process'),
    path('archivos/', ArchivosView.as_view(), name='archivo-list-create'),
    path('archivos/<int:id>/', ArchivosView.as_view(), name='archivo-detail'),
    path('compartidos/', CompartidosView.as_view(), name='compartidos-list-create'),
    path('compartidos/<int:id>/', CompartidosView.as_view(), name='compartidos-detail'),
    path('facturacion_planes/', FacturacionPlanesView.as_view(), name='facturacion_planes-list-create'),
    path('facturacion_planes/<int:id>/', FacturacionPlanesView.as_view(), name='facturacion_planes-detail'),
    path('lugares/', LugaresView.as_view(), name='lugares-list-create'),
    path('lugares/<int:id>/', LugaresView.as_view(), name='lugares-detail'),
    path('modificaciones/', ModificacionesView.as_view(), name='modificaciones-list-create'),
    path('modificaciones/<int:id>/', ModificacionesView.as_view(), name='modificaciones-detail')
]