from django.db import models
from django.contrib.auth.models import User

DIAS_SEMANA = [
    (0, "Segunda-feira"),
    (1, "Terça-feira"),
    (2, "Quarta-feira"),
    (3, "Quinta-feira"),
    (4, "Sexta-feira"),
    (5, "Sábado"),
    (6, "Domingo"),
]


class Medico(models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=50)
    crm = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nome} - {self.especialidade}"


class HorarioTrabalho(models.Model):
    medico = models.ForeignKey(
        Medico, on_delete=models.CASCADE, related_name="horarios"
    )
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    class Meta:
        ordering = ["dia_semana", "hora_inicio"]


class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nome


class Consulta(models.Model):
    STATUS_CHOICES = [
        ("Agendada", "Agendada"),
        ("Realizada", "Realizada"),
        ("Cancelada", "Cancelada"),
    ]

    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    duracao = models.IntegerField(default=30)  # em minutos
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Agendada")
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.paciente.nome} com {self.medico.nome} - {self.data_hora}"
