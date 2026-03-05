# Time Tracking API

API REST para controle de apontamento de tempo de funcionários em atividades.

Este projeto foi desenvolvido com foco didático, aplicando boas práticas de organização de código, separação de camadas e modelagem de regras de negócio.

---

## Objetivo

Simular um sistema empresarial de controle de apontamentos de tempo, permitindo:

- Cadastro de funcionários
- Cadastro de clientes
- Cadastro de atividades vinculadas a clientes
- Início, pausa, retomada e finalização de apontamentos
- Cancelamento automático de apontamentos ao desativar funcionário
- Bloqueio de novos apontamentos para atividades e clientes inativos
- Tratamento padronizado de exceções de domínio
- Métricas simples por atividade

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

```text
app/
├── models/               # Entidades e mapeamento ORM
├── crud/                 # Acesso ao banco de dados
├── services/             # Regras de negócio
├── routes/               # Camada HTTP (FastAPI)
├── database/             # Configuração de engine e sessão
├── exception_handlers.py # Tratamento global de erros
├── schemas.py            # Schemas Pydantic
├── create_tables.py      # Script de criação das tabelas
└── main.py               # Ponto de entrada da aplicação
```

---

## Fluxo interno da aplicação:
└── routes → services → crud → models

---

## Endpoints

- /clients
- /activities
- /employees
- /time_entries
- /metrics

---

## Regras de Negócio

- Um funcionário não pode possuir mais de um apontamento aberto simultaneamente.

- Funcionários inativos não podem iniciar novos apontamentos.

- Atividades inativas não permitem novos apontamentos.

- Clientes inativos bloqueiam:
- criação de novas atividades
- início de novos apontamentos vinculados às atividades daquele cliente

- O sistema controla as transições de estado do apontamento, impedindo operações inválidas como:
- pausar um apontamento já pausado
- retomar um apontamento que não esteja pausado
- finalizar um apontamento já finalizado

- Ao desativar um funcionário:
- todos os apontamentos com status INICIADO ou PAUSADO são finalizados automaticamente
- finish_type é definido como CANCELADO
- um motivo de cancelamento é registrado

- Apenas apontamentos concluídos (finish_type = CONCLUIDA) devem ser considerados para métricas futuras.

- Erros de domínio retornam respostas padronizadas contendo:
- error_code
- detail

---

## Executando Localmente
1. Criar ambiente virtual
```bash
python -m venv venv
```
2. Ativar ambiente

Windows:
```bash
venv\Scripts\activate
```
Linux/macOS:
```bash
source venv/bin/activate
```
3. Instalar dependências
```bash
pip install -r requirements.txt
```
4. Criar tabelas
```bash
python -m app.create_tables
```
5. Iniciar aplicação
```bash
uvicorn app.main:app --reload
```

6. Acesse:
```bash
http://127.0.0.1:8000/docs
```
7. Executando com Docker
- Build e execução:
```bash
docker compose up --build
```
- Criar tabelas dentro do container:
```bash
docker compose run --rm api python -m app.create_tables
```

8. Acesse:
```bash
http://127.0.0.1:8000/docs
```

---

## Estrutura do Banco de Dados

Entidades principais:

- Client

- Employee

- Activity

- TimeEntry

- TimeEntryBlock

O tempo total de um apontamento é calculado com base na soma dos blocos de tempo registrados entre início e pausa/finalização.

---

### Evolução do Projeto

O projeto continuará evoluindo com melhorias incrementais, incluindo:

Expansão de métricas e filtros

Migração para PostgreSQL

Testes automatizados

Ajustes arquiteturais conforme crescimento da aplicação

Autor

Cesar Augusto Dodó
Projeto desenvolvido com foco em consolidação de conhecimentos em backend e boas práticas de engenharia de software.