from django import forms
from .models import Cita, Paciente

from django import forms
from .models import Cita, Paciente, Dueno
import datetime

# Generamos las horas: De 9 a 20 horas (para que la última cita de 30 min sea a las 20:30 y termine a las 21:00)
HORAS_DISPONIBLES = []
for h in range(9, 21): 
   
    HORAS_DISPONIBLES.append((f"{h:02d}:00", f"{h:02d}:00"))
    HORAS_DISPONIBLES.append((f"{h:02d}:30", f"{h:02d}:30"))

class CitaForm(forms.ModelForm):
   
    hora = forms.ChoiceField(
        choices=HORAS_DISPONIBLES, 
        widget=forms.Select(attrs={'class': 'form-select'}), 
        label="Hora de Atención"
    )

    class Meta:
        model = Cita
        fields = ['veterinario', 'paciente', 'fecha', 'hora']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'veterinario': forms.Select(attrs={'class': 'form-select'}),
            'paciente': forms.Select(attrs={'class': 'form-select'}),
        }



class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'antecedentes': forms.Textarea(attrs={'rows': 3}),
        }

class ReagendarForm(forms.ModelForm):
    # 2. Definimos 'hora' explícitamente como un ChoiceField (Lista desplegable)
    hora = forms.ChoiceField(
        choices=HORAS_DISPONIBLES,
        widget=forms.Select(attrs={'class': 'form-select'}), # Estilo Bootstrap
        label="Nueva Hora"
    )

    class Meta:
        model = Cita
        fields = ['fecha', 'hora']
        widgets = {
            # Mantenemos el selector de fecha tipo calendario
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        
from .models import Dueno 

class DuenoForm(forms.ModelForm):
    class Meta:
        model = Dueno
        fields = ['nombre', 'telefono', 'email']