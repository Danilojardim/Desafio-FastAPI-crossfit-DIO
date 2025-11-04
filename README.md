# 🏋️‍♂️ WorkoutAPI — API de Treino com FastAPI

## 📘 Sobre o Projeto

A **WorkoutAPI** é uma API de competição de *crossfit* desenvolvida em **FastAPI (async)** — unindo duas paixões: **codar** e **treinar** 💪  
O objetivo do projeto é construir uma aplicação completa, moderna e performática, aplicando conceitos reais de desenvolvimento de APIs com **Python**, **PostgreSQL**, **Docker**, **SQLAlchemy**, **Alembic** e **Pydantic**.

---

## ⚙️ Tecnologias Utilizadas

| Tecnologia | Descrição |
|-------------|------------|
| **FastAPI** | Framework web moderno e de alta performance para construção de APIs com Python 3.6+ |
| **SQLAlchemy** | ORM utilizado para modelagem e persistência dos dados |
| **Alembic** | Ferramenta de versionamento e migração do banco de dados |
| **Pydantic / Pydantic Settings** | Validação e tipagem de dados baseada em modelos |
| **FastAPI Pagination** | Biblioteca para paginação automática de resultados |
| **PostgreSQL** | Banco de dados relacional utilizado |
| **Docker Compose** | Gerenciamento de containers (banco de dados PostgreSQL) |
| **Pyenv + Virtualenv** | Controle de versão do Python e isolamento de ambiente |

---

## 🚀 Execução do Projeto

### 🐍 1. Configuração do Ambiente Python

Utilize o **pyenv** para gerenciar versões do Python e criar o ambiente virtual.

```bash
# Instalar o pyenv-virtualenv (caso ainda não tenha)
pyenv install 3.11.4
pyenv virtualenv 3.11.4 workoutapi
pyenv activate workoutapi
```

Em seguida, instale as dependências:

```bash
pip install -r requirements.txt
```

---

### 🐳 2. Subindo o Banco de Dados com Docker

Antes de subir o container, verifique se o **Docker Desktop** está em execução.  
Depois, execute:

```bash
docker compose up -d
```

Isso criará e executará um container PostgreSQL conforme o arquivo `docker-compose.yml`.

Verifique se o container está rodando:

```bash
docker ps
```

---

### 🗃️ 3. Migrações com Alembic

Criação e atualização da base de dados:

```bash
# Criar uma nova migration
alembic revision --autogenerate -m "init_db"

# Aplicar as migrations
alembic upgrade head
```

---

### ▶️ 4. Rodando a API

Execute o servidor FastAPI com reload automático:

```bash
uvicorn workout_api.main:app --reload
```

Acesse no navegador:

👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📚 Estrutura do Projeto

```
workout_api/
├── alembic/                  # Controle de versões do banco
├── workout_api/
│   ├── atleta/               # Módulo de Atletas
│   ├── categorias/           # Módulo de Categorias
│   ├── centro_treinamento/   # Módulo de Centros de Treinamento
│   ├── contrib/              # Configurações e dependências
│   ├── configs/              # Banco de dados e variáveis de ambiente
│   └── main.py               # Ponto principal da aplicação
├── alembic.ini               # Configuração de migrações
├── docker-compose.yml        # Configuração do container PostgreSQL
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação (este arquivo)
```

---

## 🧠 Conceitos-Chave

### 🔹 FastAPI
> Framework web moderno, rápido e fácil de aprender, projetado para alta performance e uso intensivo de tipagem (type hints) do Python.

📖 Documentação: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

---

### 🔹 SQLAlchemy
> ORM poderoso e flexível para manipulação de banco de dados relacional com Python.

📖 Documentação: [https://docs.sqlalchemy.org/en/20/](https://docs.sqlalchemy.org/en/20/)

---

### 🔹 Alembic
> Ferramenta de migração de banco de dados para projetos com SQLAlchemy.

📖 Documentação: [https://alembic.sqlalchemy.org/en/latest/](https://alembic.sqlalchemy.org/en/latest/)

---

### 🔹 Pydantic
> Biblioteca para validação de dados e conversão de tipos baseada em anotações de tipo (type hints).

📖 Documentação: [https://docs.pydantic.dev/latest/](https://docs.pydantic.dev/latest/)

---

### 🔹 FastAPI Pagination
> Extensão para adicionar paginação de forma rápida e simples nas respostas dos endpoints.

📖 Documentação: [https://uriyyo-fastapi-pagination.netlify.app/](https://uriyyo-fastapi-pagination.netlify.app/)

---

## 🏁 Desafio Final Implementado

### ✅ Requisitos Cumpridos

| Requisito | Status | Descrição |
|------------|---------|-----------|
| **Query Parameters** | ✅ | Filtros por `nome` e `cpf` no endpoint `/atletas` |
| **Response Customizada** | ✅ | Retorno apenas de `nome`, `categoria` e `centro_treinamento` no `GET /atletas` |
| **Tratamento de Exceção (IntegrityError)** | ✅ | Retorna `HTTP 303` com mensagem “Já existe um atleta cadastrado com o CPF: x” |
| **Paginação (FastAPI Pagination)** | ✅ | Implementada paginação com `limit` e `offset` em `/atletas` |


---

## 🧩 Conclusão

Com o **FastAPI**, foi possível desenvolver uma API leve, performática e escalável, utilizando as melhores práticas modernas do ecossistema Python.

> 🚀 Projeto completo e pronto para produção!

---

📎 **Links úteis**
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [FastAPI Pagination](https://uriyyo-fastapi-pagination.netlify.app/)
