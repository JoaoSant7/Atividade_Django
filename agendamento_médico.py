from datetime import datetime, timedelta
import json


class Medico:
    def __init__(self, nome, especialidade, crm):
        self.nome = nome
        self.especialidade = especialidade
        self.crm = crm
        self.horarios_trabalho = (
            []
        )  # Lista de tuplas (dia_semana, hora_inicio, hora_fim)

    def adicionar_horario_trabalho(self, dia_semana, hora_inicio, hora_fim):
        """Adiciona horário de trabalho do médico (0=Segunda, 6=Domingo)"""
        self.horarios_trabalho.append(
            {"dia_semana": dia_semana, "hora_inicio": hora_inicio, "hora_fim": hora_fim}
        )

    def verificar_disponibilidade(self, data_hora):
        """Verifica se o médico trabalha no horário solicitado"""
        dia_semana = data_hora.weekday()
        hora = data_hora.time()

        for horario in self.horarios_trabalho:
            if horario["dia_semana"] == dia_semana:
                if horario["hora_inicio"] <= hora <= horario["hora_fim"]:
                    return True
        return False


class Paciente:
    def __init__(self, nome, cpf, telefone, email):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email


class Consulta:
    def __init__(self, medico, paciente, data_hora, duracao_minutos=30):
        self.medico = medico
        self.paciente = paciente
        self.data_hora = data_hora
        self.duracao = duracao_minutos
        self.status = "Agendada"  # Agendada, Realizada, Cancelada
        self.observacoes = ""

    def cancelar(self):
        self.status = "Cancelada"

    def realizar(self, observacoes=""):
        self.status = "Realizada"
        self.observacoes = observacoes


class SistemaAgendamento:
    def __init__(self):
        self.medicos = []
        self.pacientes = []
        self.consultas = []
        self.proximo_id = 1

    def cadastrar_medico(self, medico):
        self.medicos.append(medico)

    def cadastrar_paciente(self, paciente):
        self.pacientes.append(paciente)

    def agendar_consulta(self, medico, paciente, data_hora):
        # Verificar se médico trabalha nesse horário
        if not medico.verificar_disponibilidade(data_hora):
            return False, "Médico não trabalha neste horário"

        # Verificar conflito de horários
        for consulta in self.consultas:
            if (
                consulta.medico == medico
                and consulta.data_hora == data_hora
                and consulta.status != "Cancelada"
            ):
                return False, "Horário já ocupado"

        # Criar consulta
        nova_consulta = Consulta(medico, paciente, data_hora)
        self.consultas.append(nova_consulta)
        return True, "Consulta agendada com sucesso"

    def cancelar_consulta(self, consulta):
        consulta.cancelar()
        return True, "Consulta cancelada"

    def listar_consultas_medico(self, medico, data_inicio=None):
        """Lista consultas de um médico, opcionalmente filtrando por data"""
        resultado = []
        for consulta in self.consultas:
            if consulta.medico == medico:
                if (
                    data_inicio is None
                    or consulta.data_hora.date() >= data_inicio.date()
                ):
                    resultado.append(consulta)
        return resultado

    def historico_paciente(self, paciente):
        """Retorna histórico completo do paciente"""
        historico = []
        for consulta in self.consultas:
            if consulta.paciente == paciente:
                historico.append(consulta)
        # Ordenar por data (mais recente primeiro)
        historico.sort(key=lambda x: x.data_hora, reverse=True)
        return historico

    def horarios_disponiveis(self, medico, data):
        """Retorna horários disponíveis para um médico em uma data específica"""
        disponiveis = []

        # Encontrar horário de trabalho do médico nesse dia
        dia_semana = data.weekday()
        horario_trabalho = None

        for horario in medico.horarios_trabalho:
            if horario["dia_semana"] == dia_semana:
                horario_trabalho = horario
                break

        if not horario_trabalho:
            return disponiveis  # Médico não trabalha nesse dia

        # Gerar slots de 30 minutos
        hora_atual = datetime.combine(data, horario_trabalho["hora_inicio"])
        hora_fim = datetime.combine(data, horario_trabalho["hora_fim"])

        while hora_atual < hora_fim:
            # Verificar se horário está livre
            ocupado = False
            for consulta in self.consultas:
                if (
                    consulta.medico == medico
                    and consulta.data_hora == hora_atual
                    and consulta.status != "Cancelada"
                ):
                    ocupado = True
                    break

            if not ocupado:
                disponiveis.append(hora_atual)

            hora_atual += timedelta(minutes=30)

        return disponiveis


# Exemplo de uso e demonstração
if __name__ == "__main__":
    sistema = SistemaAgendamento()

    # Cadastrar médicos
    dr_silva = Medico("Dr. Aureliano Silva ", "Cardiologia", "12345/SP")
    dr_silva.adicionar_horario_trabalho(
        0,
        datetime.strptime("08:00", "%H:%M").time(),
        datetime.strptime("17:00", "%H:%M").time(),
    )  # Segunda
    dr_silva.adicionar_horario_trabalho(
        2,
        datetime.strptime("08:00", "%H:%M").time(),
        datetime.strptime("17:00", "%H:%M").time(),
    )  # Quarta

    dra_oliveira = Medico("Dra. Maria Oliveira", "Pediatria", "54321/SP")
    dra_oliveira.adicionar_horario_trabalho(
        1,
        datetime.strptime("09:00", "%H:%M").time(),
        datetime.strptime("16:00", "%H:%M").time(),
    )  # Terça
    dra_oliveira.adicionar_horario_trabalho(
        3,
        datetime.strptime("09:00", "%H:%M").time(),
        datetime.strptime("16:00", "%H:%M").time(),
    )  # Quinta

    sistema.cadastrar_medico(dr_silva)
    sistema.cadastrar_medico(dra_oliveira)

    # Cadastrar pacientes
    paciente1 = Paciente(
        "Carlos Souza", "123.456.789-00", "(11) 99999-9999", "carlos@email.com"
    )
    paciente2 = Paciente(
        "Ana Santos", "987.654.321-00", "(11) 88888-8888", "ana@email.com"
    )

    sistema.cadastrar_paciente(paciente1)
    sistema.cadastrar_paciente(paciente2)

    # Agendar consultas
    data_consulta1 = datetime(2024, 1, 15, 10, 0)  # Segunda, 10:00
    sucesso, mensagem = sistema.agendar_consulta(dr_silva, paciente1, data_consulta1)
    print(f"Agendamento 1: {mensagem}")

    data_consulta2 = datetime(2024, 1, 16, 14, 0)  # Terça, 14:00
    sucesso, mensagem = sistema.agendar_consulta(
        dra_oliveira, paciente2, data_consulta2
    )
    print(f"Agendamento 2: {mensagem}")

    # Tentar agendar no mesmo horário (deve falhar)
    sucesso, mensagem = sistema.agendar_consulta(dr_silva, paciente2, data_consulta1)
    print(f"Agendamento conflitante: {mensagem}")

    # Mostrar horários disponíveis
    print("\nHorários disponíveis Dr. Silva para 15/01/2024:")
    disponiveis = sistema.horarios_disponiveis(dr_silva, datetime(2024, 1, 15))
    for horario in disponiveis[:5]:  # Mostrar apenas 5 primeiros
        print(f"  - {horario.strftime('%H:%M')}")

    # Histórico do paciente
    print(f"\nHistórico do paciente {paciente1.nome}:")
    historico = sistema.historico_paciente(paciente1)
    for consulta in historico:
        print(
            f"  - {consulta.data_hora.strftime('%d/%m/%Y %H:%M')} com {consulta.medico.nome}"
        )

    # Interface simplificada
    def menu_principal():
        print("\n" + "=" * 50)
        print("SISTEMA DE AGENDAMENTO - CONSULTÓRIO MÉDICO")
        print("=" * 50)
        print("1. Agendar consulta")
        print("2. Cancelar consulta")
        print("3. Ver horários disponíveis")
        print("4. Histórico do paciente")
        print("5. Sair")

        opcao = input("\nEscolha uma opção: ")
        return opcao

    # Simulação de interface (para demonstração)
    while True:
        opcao = menu_principal()

        if opcao == "1":
            print("\n--- AGENDAR CONSULTA ---")
            # Aquir seria a lógica completa de agendamento
            print("Funcionalidade de agendamento ativada")

        elif opcao == "5":
            print("Saindo do sistema...")
            break
        else:
            print("Opção em desenvolvimento...")
