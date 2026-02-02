from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Estudante(Base):
    __tablename__ = 'estudantes'

    id = Column(Integer, primary_key=True, index=True)
    # Na transcrição ele usa 'nome', mas no JSON da aula 01 estava 'name'.
    # Mantive 'nome' para seguir o vídeo, mas mantenha a consistência depois!
    nome = Column(String(100), nullable=False)
    idade = Column(Integer)

class Matricula(Base):
    __tablename__ = 'matriculas'

    id = Column(Integer, primary_key=True, index=True)
    # AQUI ESTÁ O PULO DO GATO: A ForeignKey deve apontar para 'tabela.coluna'
    # Na transcrição diz 'estudante.id', mas o nome da tabela acima é 'estudantes'.
    student_id = Column(Integer, ForeignKey('estudantes.id'))
    nome_disciplina = Column(String(100), nullable=False)