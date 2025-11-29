from django.core.management.base import BaseCommand
from agendamento.models import Medico, HorarioTrabalho, Paciente, Consulta
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Popula o banco com dados de exemplo"

    def handle(self, *args, **options):
        # Criar médicos
        dr_silva = Medico.objects.create(
            nome="Dr. Aureliano Silva", especialidade="Cardiologia", crm="12345/SP"
        )

        dra_oliveira = Medico.objects.create(
            nome="Dra. Maria Oliveira", especialidade="Pediatria", crm="54321/SP"
        )

        # Horários de trabalho
        HorarioTrabalho.objects.create(
            medico=dr_silva,
            dia_semana=0,  # Segunda
            hora_inicio="08:00",
            hora_fim="17:00",
        )

        HorarioTrabalho.objects.create(
            medico=dr_silva,
            dia_semana=2,  # Quarta
            hora_inicio="08:00",
            hora_fim="17:00",
        )

        # ... adicionar mais dados conforme necessário

        self.stdout.write(self.style.SUCCESS("Dados populados com sucesso!"))
