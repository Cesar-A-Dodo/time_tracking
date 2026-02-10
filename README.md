# Time Tracking API

API REST para controle de apontamento de tempo de funcionários em atividades/tarefas.

Este projeto foi desenvolvido com foco em:
- clareza das regras de negócio
- controle rigoroso de estados
- base sólida para evolução futura do sistema

-----

## Visão Geral

A Time Tracking API permite controlar o ciclo completo de trabalho de funcionários, desde o início de uma tarefa até sua finalização.

Funcionalidades principais:
- Cadastro de funcionários
- Cadastro de atividades (tarefas)
- Início de apontamento de tempo
- Pausa e reinício de apontamento
- Finalização de apontamento (concluído ou cancelado)
- Consulta de histórico por funcionário

Todo o fluxo é guiado por **regras explícitas de negócio**, evitando inconsistências como:
- dois apontamentos ativos para o mesmo funcionário
- finalizações inválidas
- reinícios indevidos

-----

## Tecnologias Utilizadas

- Python 3.12+
- FastAPI
- Pydantic
- SQLite (fase teste)
- Uvicorn

-----

## Estados do Apontamento

- Um apontamento pode assumir os seguintes estados:

- "CRIADO"
- "INICIADO"
- "PAUSADO"
- "FINALIZADO"

Tipos de finalização possíveis:

- "CONCLUIDA"
- "TAREFA_CANCELADA"

-----

## Regras de Negócio (Resumo)

- Um funcionário pode ter vários apontamentos, mas **apenas um ativo por vez**
- Um apontamento não pode ser finalizado sem ter sido iniciado
- Um apontamento pausado pode ser finalizado como **tarefa cancelada**
- Uma atividade pode ser usada por vários funcionários
- Atividades semelhantes podem existir para clientes diferentes (IDs distintos)

-----

## Como Executar o Projeto

### Criar e ativar o ambiente virtual

python -m venv venv

Windows
venv\Scripts\activate

Linux / macOS
source venv/bin/activate

- Instalar as dependências
pip install -r requirements.txt
- Executar a aplicação
uvicorn app.main:app --reload

- A API ficará disponível em:
http://127.0.0.1:8000

- Documentação automática (Swagger):
http://127.0.0.1:8000/docs

-----

## Status do Projeto: Em desenvolvimento

-----

## Etapas concluídas:

Planejamento de regras de negócio

Modelo de estados

Casos de teste de negócio (conceituais)

Schemas Pydantic

Estrutura inicial da API

Configuração de ambiente

-----

## Próxima etapa:

Persistência e modelagem do banco de dados (SQLite)

- Observações
Este projeto foi construído priorizando entendimento, organização e escalabilidade.

Decisões de arquitetura e regras de negócio foram pensadas antes da implementação para evitar retrabalho no futuro.