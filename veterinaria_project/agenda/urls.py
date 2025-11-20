from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_recepcion, name='panel_recepcion'),
    path('cancelar/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
    path('replanificar/', views.lista_replanificacion, name='lista_replanificacion'),
    path('cita/reagendar/<int:cita_id>/', views.reagendar_cita, name='reagendar_cita'),
    ]