from django.contrib import admin
from .models import Medico, HorarioTrabalho, Paciente, Consulta


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ["nome", "especialidade", "crm"]
    search_fields = ["nome", "especialidade"]


@admin.register(HorarioTrabalho)
class HorarioTrabalhoAdmin(admin.ModelAdmin):
    list_display = ["medico", "get_dia_semana", "hora_inicio", "hora_fim"]
    list_filter = ["dia_semana", "medico"]

    def get_dia_semana(self, obj):
        return obj.get_dia_semana_display()


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ["nome", "cpf", "telefone", "email"]
    search_fields = ["nome", "cpf"]


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ["paciente", "medico", "data_hora", "status"]
    list_filter = ["status", "medico", "data_hora"]
    date_hierarchy = "data_hora"
