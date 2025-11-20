from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cita
from django import forms


# FORMULARIO DE REAGENDAMIENTO
class ReagendarForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha', 'hora']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }



# HU004 / HU002 – PANEL PRINCIPAL

def panel_recepcion(request):
    """
    Muestra solo citas activas.
    No aparecen las canceladas o eliminadas.
    """
    citas = Cita.objects.exclude(
        estado__in=['CANCELADA_VET', 'ELIMINADA']
    ).order_by('fecha', 'hora')

    return render(request, 'agenda/panel.html', {'citas': citas})



# HU005 – CANCELAR CITA (VET)
def cancelar_cita(request, cita_id):
    """
    Veterinario cancela una cita.
    Genera alerta y envía la cita a replanificación.
    """
    cita = get_object_or_404(Cita, id=cita_id)

    cita.estado = 'CANCELADA_VET'
    cita.save()

   
    mensaje = (
        f"ALERTA: El veterinario {cita.veterinario.nombre} canceló la hora de "
        f"{cita.paciente.nombre}. Contactar a {cita.paciente.dueno.nombre} "
        f"al {cita.paciente.dueno.telefono}."
    )
    messages.warning(request, mensaje)

    return redirect('lista_replanificacion')


# HU006 – LISTA DE REPLANIFICACIÓN
def lista_replanificacion(request):
    """
    Muestra citas canceladas por veterinario para re-agendar.
    (Requisito HU006)
    """
    citas_canceladas = Cita.objects.filter(
        estado='CANCELADA_VET'
    ).order_by('fecha', 'hora')

    return render(request, 'agenda/replanificar.html', {
        'citas': citas_canceladas
    })



# HU006 – REAGENDAR CITA
def reagendar_cita(request, cita_id):
    """
    Permite replanificar la hora de una cita cancelada.
    """
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        form = ReagendarForm(request.POST, instance=cita)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.estado = 'PENDIENTE'
            cita.save()

            messages.success(request, "La cita fue reagendada correctamente.")
            return redirect('panel_recepcion')
    else:
        form = ReagendarForm(instance=cita)

    return render(request, 'agenda/reagendar.html', {
        'form': form,
        'cita': cita
    })