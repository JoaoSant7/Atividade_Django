from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Medico, Consulta, HorarioTrabalho, Paciente


def home(request):
    medicos = Medico.objects.all()
    consultas = Consulta.objects.filter(status="Agendada").order_by("data_hora")[:5]

    context = {
        "medicos": medicos,
        "proximas_consultas": consultas,
    }
    return render(request, "agendamento/home.html", context)


def medicos_list(request):
    medicos = Medico.objects.all()
    return render(request, "agendamento/medicos.html", {"medicos": medicos})


def medico_detail(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)
    horarios = medico.horarios.all()

    # Próximos 7 dias para agendamento
    dias_disponiveis = []
    for i in range(7):
        dia = timezone.now().date() + timedelta(days=i)
        dia_semana = dia.weekday()
        if horarios.filter(dia_semana=dia_semana).exists():
            dias_disponiveis.append(dia)

    context = {
        "medico": medico,
        "horarios": horarios,
        "dias_disponiveis": dias_disponiveis,
    }
    return render(request, "agendamento/medico_detail.html", context)


def horarios_disponiveis(request, medico_id, data):
    medico = get_object_or_404(Medico, id=medico_id)
    data_obj = datetime.strptime(data, "%Y-%m-%d").date()
    dia_semana = data_obj.weekday()

    # Verificar se médico trabalha nesse dia
    horario_trabalho = HorarioTrabalho.objects.filter(
        medico=medico, dia_semana=dia_semana
    ).first()

    horarios_disponiveis = []

    if horario_trabalho:
        # Gerar slots de 30 minutos
        hora_atual = datetime.combine(data_obj, horario_trabalho.hora_inicio)
        hora_fim = datetime.combine(data_obj, horario_trabalho.hora_fim)

        while hora_atual < hora_fim:
            # Verificar se não há consulta agendada
            consulta_existente = Consulta.objects.filter(
                medico=medico, data_hora=hora_atual, status="Agendada"
            ).exists()

            if not consulta_existente:
                horarios_disponiveis.append(hora_atual.strftime("%H:%M"))

            hora_atual += timedelta(minutes=30)

    return JsonResponse({"horarios": horarios_disponiveis})


def consultas_list(request):
    consultas = Consulta.objects.all().order_by("-data_hora")
    return render(request, "agendamento/consultas.html", {"consultas": consultas})
