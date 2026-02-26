# Time Tracking API

API REST para controle de apontamento de tempo de funcionários em atividades.

Este projeto foi desenvolvido com foco didático, aplicando boas práticas de organização de código, separação de camadas e modelagem de regras de negócio.

---

## Objetivo

Simular um sistema empresarial de controle de apontamentos de tempo, permitindo:

- Cadastro de funcionários
- Cadastro de atividades
- Início, pausa, retomada e finalização de apontamentos
- Cancelamento automático de apontamentos ao desativar funcionário
- Bloqueio de novos apontamentos para atividades inativas
- Tratamento padronizado de exceções de domínio

---

## Tecnologias

- Python 3.11+
- FastAPI
- SQLAlchemy (ORM)
- SQLite
- Uvicorn
- Docker

---

## Arquitetura

O projeto está organizado em camadas, separando responsabilidades:


app/
├── models/    # Entidades e mapeamento ORM
├── crud/    # Acesso ao banco de dados
├── services/    # Regras de negócio
├── routes/    # Camada HTTP (FastAPI)
├── database/    # Configuração de engine e sessão
├── exception_handlers.py    # Tratamento global de erros
├── schemas.py    # Modelos Pydantic
└── main.py    # Ponto de entrada da aplicação


### Fluxo interno da aplicação:


- routes → services → crud → models


---

## Regras de Negócio

- Um funcionário não pode possuir mais de um apontamento aberto simultaneamente.
- Funcionários inativos não podem iniciar novos apontamentos.
- Atividades inativas não permitem novos apontamentos.
- O sistema controla as transições de estado do apontamento, impedindo operações inválidas como:
  - Pausar um apontamento já pausado.
  - Retomar um apontamento que não esteja pausado.
  - Finalizar um apontamento já finalizado.
- Ao desativar um funcionário:
  - Todos os apontamentos com status `INICIADO` ou `PAUSADO` são finalizados automaticamente.
  - O `finish_type` é definido como `CANCELADO`.
  - Um motivo de cancelamento é registrado.
- Apenas apontamentos concluídos (`finish_type = CONCLUIDA`) devem ser considerados para métricas futuras.
- Erros de domínio retornam respostas padronizadas contendo:
  - `error_code`
  - `detail`

---

## Executando Localmente

### 1. Criar ambiente virtual

```bash
python -m venv venv

- Ativar:
Windows: venv\Scripts\activate
Linux/macOS: source venv/bin/activate

- Instalar dependências
pip install -r requirements.txt

- Criar tabelas
python -m app.create_tables

- Iniciar aplicação
uvicorn app.main:app --reload

Acesse:
http://127.0.0.1:8000/docs

Executando com Docker

- Build e execução
docker compose up --build
- Criar tabelas dentro do container
docker compose run --rm api python -m app.create_tables

Acesse:
http://127.0.0.1:8000/docs
```
### Estrutura do Banco de Dados

Entidades principais:

- Employee

- Activity

- TimeEntry

- TimeEntryBlock

O tempo total de um apontamento é calculado com base na soma dos blocos de tempo registrados entre início e pausa/finalização.

### Evolução do Projeto

O projeto continuará evoluindo com melhorias incrementais, incluindo:

- Métricas de desempenho por atividade

- Migração para PostgreSQL

- Testes automatizados

- Ajustes arquiteturais conforme crescimento da aplicação

### Autor

Cesar Augusto Dodó
Projeto desenvolvido com foco em consolidação de conhecimentos em backend e boas práticas de engenharia de software.