from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Cita, Veterinario
from .forms import CitaForm, PacienteForm, ReagendarForm
import datetime
from datetime import time

# --- HU001 y HU002: Ver disponibilidad y Agendar hora ---
def agendar_hora(request):
    """
    Permite buscar disponibilidad visualmente (HU001) y agendar la hora (HU002).
    Controla horario de atención (9:00-21:00) y disponibilidad por veterinario.
    """
    citas_ocupadas = Cita.objects.filter(estado='PENDIENTE').order_by('fecha', 'hora')
    
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita_nueva = form.save(commit=False)
            
            # --- VALIDACIÓN 1: Rango Horario (09:00 a 21:00) ---
            hora_inicio_atencion = time(9, 0)  # 09:00 AM
            hora_fin_atencion = time(21, 0)    # 09:00 PM
            
            if not (hora_inicio_atencion <= cita_nueva.hora <= hora_fin_atencion):
                messages.error(request, "Error: El horario de atención es de 09:00 a 21:00 hrs.")
                return render(request, 'agenda/agendar.html', {
                    'form': form, 
                    'citas_ocupadas': citas_ocupadas
                })

            # --- VALIDACIÓN 2: Disponibilidad del Veterinario (Simultaneidad) ---
            # Si tienes 3 veterinarios, el sistema permitirá guardar 3 citas a las 10:00
            # siempre que sean con veterinarios distintos. Aquí validamos que EL ELEGIDO no esté ocupado.
            existe_cita = Cita.objects.filter(
                veterinario=cita_nueva.veterinario,
                fecha=cita_nueva.fecha,
                hora=cita_nueva.hora,
                estado='PENDIENTE'
            ).exists()
            
            if existe_cita:
                messages.error(request, f"El Dr. {cita_nueva.veterinario.nombre} ya está ocupado a esa hora. Por favor seleccione otro veterinario u otro horario.")
            else:
                cita_nueva.save()
                messages.success(request, "Hora agendada correctamente.")
                return redirect('panel_recepcion')
    else:
        form = CitaForm()

    return render(request, 'agenda/agendar.html', {
        'form': form,
        'citas_ocupadas': citas_ocupadas 
    })  
# --- HU003: Crear la ficha del paciente ---
def crear_paciente(request):
    """
    Permite registrar un nuevo paciente y su dueño en el sistema.
    """
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            messages.success(request, f"Ficha creada para {paciente.nombre}")
            return redirect('panel_recepcion')
    else:
        form = PacienteForm()
    
    return render(request, 'agenda/crear_paciente.html', {'form': form})

# --- HU004: Cancelar hora (Por Cliente/Recepcionista) ---
def cancelar_cita_cliente(request, cita_id):
    """
    Libera el cupo cuando el cliente avisa que no va.
    Simplemente cambiamos el estado o podríamos borrarla. 
    Aquí la marcamos como cancelada por cliente.
    """
    cita = get_object_or_404(Cita, id=cita_id)
    cita.estado = 'CANCELADA_CLIENTE'
    cita.save()
    messages.info(request, "La hora ha sido cancelada y el cupo liberado.")
    return redirect('panel_recepcion')

# --- HU005 y HU007: Cancelar hora (Por Veterinario) ---
def cancelar_cita_veterinario(request, cita_id):
    """
    El vet cancela (HU005) o avisa indisponibilidad (HU007).
    Esto dispara la alerta y mueve la cita a la lista de replanificación.
    """
    cita = get_object_or_404(Cita, id=cita_id)
    cita.estado = 'CANCELADA_VET'
    cita.save()

    # HU005: Alerta de comunicación
    mensaje = (
        f"ALERTA CRÍTICA: El Dr. {cita.veterinario.nombre} canceló la atención de {cita.paciente.nombre}. "
        f"Llamar a {cita.paciente.dueno.nombre} al {cita.paciente.dueno.telefono}."
    )
    messages.warning(request, mensaje)
    
    return redirect('lista_replanificacion')

# --- PANEL PRINCIPAL (Vista general) ---
def panel_recepcion(request):
    """
    Muestra las citas del día y futuras.
    """
    citas = Cita.objects.filter(estado='PENDIENTE').order_by('fecha', 'hora')
    return render(request, 'agenda/panel.html', {'citas': citas})

# --- HU006: Replanificar horas ---
def lista_replanificacion(request):
    """
    Muestra SOLO las citas canceladas por el veterinario que requieren acción.
    """
    citas = Cita.objects.filter(estado='CANCELADA_VET').order_by('fecha')
    return render(request, 'agenda/lista_replanificacion.html', {'citas': citas})

def reagendar_cita(request, cita_id):
    """
    Formulario para asignar nueva fecha a una cita cancelada por vet.
    HU006 pide mostrar antecedentes.
    """
    cita = get_object_or_404(Cita, id=cita_id)
    
    if request.method == 'POST':
        form = ReagendarForm(request.POST, instance=cita)
        if form.is_valid():
            nueva_cita = form.save(commit=False)
            nueva_cita.estado = 'PENDIENTE' # Vuelve a estar activa
            nueva_cita.save()
            messages.success(request, "La cita ha sido replanificada exitosamente.")
            return redirect('lista_replanificacion')
    else:
        form = ReagendarForm(instance=cita)

    return render(request, 'agenda/reagendar.html', {
        'form': form,
        'cita': cita # Pasamos el objeto cita para ver antecedentes en HTML
    })
    
    
from .models import Dueno
from .forms import DuenoForm

# --- GESTIÓN DE DUEÑOS ---

def lista_duenos(request):
    """
    Muestra todos los dueños registrados y botón para eliminar.
    """
    duenos = Dueno.objects.all().order_by('nombre')
    return render(request, 'agenda/lista_duenos.html', {'duenos': duenos})

def crear_dueno(request):
    """
    Formulario para agregar un nuevo dueño.
    """
    if request.method == 'POST':
        form = DuenoForm(request.POST)
        if form.is_valid():
            dueno = form.save()
            messages.success(request, f"Dueño {dueno.nombre} agregado correctamente.")
            # Redirigimos a la lista de dueños o directo a crear paciente si prefieres
            return redirect('lista_duenos')
    else:
        form = DuenoForm()
    
    return render(request, 'agenda/crear_dueno.html', {'form': form})

def eliminar_dueno(request, dueno_id):
    """
    Elimina un dueño. 
    OJO: Si borras al dueño, se borrarán sus mascotas y citas (por el on_delete=CASCADE del modelo).
    """
    dueno = get_object_or_404(Dueno, id=dueno_id)
    dueno.delete()
    messages.success(request, "Dueño eliminado del sistema.")
    return redirect('lista_duenos')