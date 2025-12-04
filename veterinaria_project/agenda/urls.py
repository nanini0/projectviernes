from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_recepcion, name='panel_recepcion'),
    path('agendar/', views.agendar_hora, name='agendar_hora'),
    path('paciente/nuevo/', views.crear_paciente, name='crear_paciente'),
    
    # Acciones de cancelación
    path('cancelar/cliente/<int:cita_id>/', views.cancelar_cita_cliente, name='cancelar_cita_cliente'),
    path('cancelar/vet/<int:cita_id>/', views.cancelar_cita_veterinario, name='cancelar_cita_veterinario'),
    
    # Replanificación
    path('replanificacion/', views.lista_replanificacion, name='lista_replanificacion'),
    path('reagendar/<int:cita_id>/', views.reagendar_cita, name='reagendar_cita'),
    
    # Gestión de Dueños
    path('duenos/', views.lista_duenos, name='lista_duenos'),
    path('duenos/nuevo/', views.crear_dueno, name='crear_dueno'),
    path('duenos/eliminar/<int:dueno_id>/', views.eliminar_dueno, name='eliminar_dueno'),
]