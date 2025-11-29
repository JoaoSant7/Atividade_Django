# Visão Geral

O sistema pretende resolver o seguinte cenário: uma clínica médica precisa abandonar a agenda de papel.

# Requisitos Funcionais

- Médicos sejam registrados;
- Horários fixos de trabalho dos médicos sejam registrados;
- Pacientes sejam registrados;
- Função de exibir um histórico das consultas de cada paciente.

## Requisitos Não-Funcionais

- O sistema deve funcionar em qualquer sistema operacional (e.g _Linux_, _MacOS_, _FreeBSD_, etc)

# Regras e Validações

- Um médico não pode possuir consultas em horários conflitantes;
- Consultas só podem ser agendadas dentro do horário de trabalho do médico;
- Não permitir agendamentos com menos de 2 horas de antecedência;
- Não podem haver dois pacientes com o mesmo CPF;
- Não podem haver dois médicos com o mesmo CRM;
- O médico não pode possuir horários fora do horário de funcionamento do consultório.

## Regras de status

- Consultas só poderão ser canceladas até 24h antes do horário da consulta
- Status automático: a consulta será marcada como "Realizada"
