# Time Tracking API

API REST para controle de apontamento de tempo de funcionários em atividades.

Projeto desenvolvido com foco em arquitetura limpa, regras de negócio explícitas e evolução incremental.

---

## Principais Funcionalidades

- Cadastro de funcionários
- Cadastro de atividades
- Início de apontamento
- Pausa e retomada
- Finalização (concluído ou cancelado)
- Controle de múltiplos blocos de tempo
- Cálculo automático do tempo total executado

---

## Modelo de Tempo

O sistema utiliza **block-based time tracking**:

- Cada início ou retomada cria um bloco
- Cada pausa ou finalização fecha o bloco
- O tempo total é a soma de todos os blocos fechados

Esse modelo permite precisão mesmo em cenários com múltiplas pausas.

---

## Regras de Negócio

- Um funcionário pode ter apenas um apontamento ativo por vez
- Apontamentos finalizados não podem ser alterados
- Blocos abertos são automaticamente fechados ao pausar ou finalizar
- Cancelamento encerra o apontamento com tipo de finalização específico
- Exclusão física de apontamentos não é permitida para preservar métricas

---

## Arquitetura

Estrutura baseada em separação de responsabilidades:

- `models/` → ORM (SQLAlchemy 2.0)
- `crud/` → Persistência
- `services/` → Regras de negócio
- `schemas.py` → Validação (Pydantic)
- `tests/` → Testes de fluxo real

---

## Tecnologias

- Python 3.12+
- FastAPI
- SQLAlchemy 2.0
- Pydantic
- SQLite (desenvolvimento)

---

## Executando o Projeto

```bash

python -m venv venv

venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/macOS

pip install -r requirements.txt
uvicorn app.main:app --reload

```

Acesse:

API: http://127.0.0.1:8000

Docs: http://127.0.0.1:8000/docs

---

### Status

Em desenvolvimento contínuo.

Próximos passos:

- Métricas por atividade

- Métricas por funcionário

- Endpoints completos

- Evolução para ambiente de produção