from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Tabela associativa para N:N entre Estudante e Disciplina
estudante_disciplina = Table(
    'estudante_disciplina',
    Base.metadata,
    Column('estudante_id', Integer, ForeignKey('estudantes.id')),
    Column('disciplina_id', Integer, ForeignKey('disciplinas.id'))
)

class Estudante(Base):
    __tablename__ = 'estudantes'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer)
    
    # 1:1 com Perfil
    perfil = relationship("Perfil", back_populates="estudante", uselist=False, cascade="all, delete-orphan")
    
    # 1:N com Matriculas
    matriculas = relationship("Matricula", back_populates="estudante")
    
    # N:N com Disciplinas
    disciplinas = relationship("Disciplina", secondary=estudante_disciplina, back_populates="estudantes")

class Perfil(Base):
    __tablename__ = 'perfis'
    
    id = Column(Integer, primary_key=True, index=True)
    idade = Column(Integer)
    endereco = Column(String(100))
    estudante_id = Column(Integer, ForeignKey('estudantes.id'), unique=True)
    
    estudante = relationship("Estudante", back_populates="perfil")

class Matricula(Base):
    __tablename__ = 'matriculas'

    id = Column(Integer, primary_key=True, index=True)
    estudante_id = Column(Integer, ForeignKey('estudantes.id'))
    nome_disciplina = Column(String(100), nullable=False)
    
    # Relacionamento de volta para Estudante
    estudante = relationship("Estudante", back_populates="matriculas")

class Disciplina(Base):
    __tablename__ = 'disciplinas'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    
    # N:N de volta para Estudante
    estudantes = relationship("Estudante", secondary=estudante_disciplina, back_populates="disciplinas")