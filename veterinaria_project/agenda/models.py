from django.db import models

# Create your models here.
from django.db import models

class Veterinario(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100, default="General")

    def __str__(self):
        return self.nombre

class Dueno(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Paciente(models.Model):
    nombre = models.CharField(max_length=50)
    especie = models.CharField(max_length=50) 
    dueno = models.ForeignKey(Dueno, on_delete=models.CASCADE)
    antecedentes = models.TextField(help_text="Historial médico relevante", blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.dueno.nombre})"

class Cita(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA_VET', 'Cancelada por Veterinario'),
    ]

    veterinario = models.ForeignKey(Veterinario, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    def __str__(self):
        return f"Cita: {self.paciente} con {self.veterinario} - {self.fecha}"