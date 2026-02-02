# Sistema de Gestão Escolar (API)

Este projeto é uma API RESTful para gestão escolar, desenvolvida como parte do curso de **Persistência de Dados com FastAPI e SQLAlchemy** da **Alura**.

O código evoluiu além do escopo básico da aula, incorporando boas práticas de engenharia de software e funcionalidades completas de CRUD.

## 🚀 Funcionalidades

- **Gestão Completa (CRUD)**:
  - **Estudantes**: Cadastro com validação de email e idade, listagem, atualização e remoção.
  - **Professores**: Gestão de corpo docente.
  - **Disciplinas**: Criação de matérias e vínculo com professores.
- **Relacionamentos Avançados**:
  - **1:1**: Estudante <-> Perfil.
  - **1:N**: Professor -> Disciplinas | Estudante -> Matrículas.
  - **N:N**: Estudantes <-> Disciplinas (Inscrição).
- **Performance e Qualidade**:
  - Utilização de `joinedload` para otimização de queries (redução do problema N+1).
  - Validação rigorosa de dados com **Pydantic** (`EmailStr`, `PositiveInt`).
  - Banco de dados relacional com **SQLAlchemy 2.0**.

## 🛠️ Tecnologias

- **Python 3.10+**
- **FastAPI**: Framework web moderno e rápido.
- **SQLAlchemy**: ORM para persistência de dados.
- **Pydantic**: Validação de esquemas.
- **PostgreSQL / SQLite**: Suporte a banco de dados.

## 📦 Como Rodar

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/FuriaLLMs/persistenciadedadosalura.git
   cd persistenciadedadosalura
   ```

2. **Crie e ative o ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**:
   ```bash
   uvicorn main:app --reload
   ```

A documentação interativa (Swagger UI) estará disponível em: `http://127.0.0.1:8000/docs`.

## 📚 Origem e Créditos

Este projeto foi iniciado seguindo os passos da formação **Desenvolvedor Backend Python** da **Alura**, especificamente no módulo de persistência de dados. 

As funcionalidades extras (Validação de Email, Entidade Professor, Otimizações de Query e Delete/Update endpoints) foram implementadas para consolidar o conhecimento e criar uma aplicação mais robusta.
