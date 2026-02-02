from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# String de Conexão: protocolo://usuario:senha@url:porta/nome_do_banco
# IMPORTANTE: Se sua senha do postgres não for 'postgres', altere aqui.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/escola"

# 1. Engine: O motor que abre a conexão real com o banco
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 2. SessionLocal: A fábrica de sessões.
# Cada requisição (usuario acessando o site) vai criar uma instância disso.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base: A classe mãe.
# Todos os seus modelos (Estudante, Matricula) vão herdar dessa classe
# para que o SQLAlchemy saiba que eles são tabelas do banco.
Base = declarative_base()