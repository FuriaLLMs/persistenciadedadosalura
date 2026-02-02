from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Estudante(Base):
    __tablename__ = 'estudantes'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer)
    
    # Relacionamento 1:1 com Perfil
    perfil = relationship("Perfil", back_populates="estudante", uselist=False, cascade="all, delete-orphan")

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