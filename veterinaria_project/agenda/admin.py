from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Veterinario, Dueno, Paciente, Cita

# Registramos los modelos para que aparezcan en /admin
admin.site.register(Veterinario)
admin.site.register(Dueno)
admin.site.register(Paciente)

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'veterinario', 'fecha', 'hora', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('paciente__nombre',)