# models.py exemplo
class Medico(models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=50)
    crm = models.CharField(max_length=20, unique=True)


class HorarioTrabalho(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
