from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importando nossos arquivos locais
import models
import schemas
from database import SessionLocal, engine

# Cria as tabelas no banco de dados automaticamente se não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependência: Garante que o banco abre e FECHA a conexão a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROTAS DE ESTUDANTES ---

# 1. POST: Criar Estudante
@app.post("/estudantes/", response_model=schemas.EstudanteResponse)
def create_student(student: schemas.EstudanteCreate, db: Session = Depends(get_db)):
    # Converte o Pydantic (JSON) para o Modelo do Banco (SQLAlchemy)
    db_student = models.Estudante(**student.model_dump())
    
    db.add(db_student)      # Adiciona na "fila" do banco
    db.commit()             # Confirma a gravação (Salva de verdade)
    db.refresh(db_student)  # Atualiza o objeto com o ID gerado pelo banco
    
    return db_student

# 2. GET: Listar Estudantes
@app.get("/estudantes/", response_model=List[schemas.EstudanteResponse])
def read_students(db: Session = Depends(get_db)):
    # SELECT * FROM estudantes;
    students = db.query(models.Estudante).all()
    return students

# 3. GET: Buscar Estudante por ID
@app.get("/estudantes/{estudante_id}", response_model=schemas.EstudanteResponse)
def read_student(estudante_id: int, db: Session = Depends(get_db)):
    # Faz a consulta: SELECT * FROM estudantes WHERE id = estudante_id
    db_student = db.query(models.Estudante).filter(models.Estudante.id == estudante_id).first()
    
    # Validação importante: se o ID não existir, retornamos erro 404
    if db_student is None:
        raise HTTPException(status_code=404, detail="Estudante não encontrado")
    
    return db_student

# --- ROTAS DE PERFIS ---

@app.post("/perfis/", response_model=schemas.PerfilResponse, status_code=status.HTTP_201_CREATED)
def create_perfil(perfil: schemas.PerfilCreate, db: Session = Depends(get_db)):
    # Verifica se o estudante existe
    db_estudante = db.query(models.Estudante).filter(models.Estudante.id == perfil.estudante_id).first()
    if not db_estudante:
        raise HTTPException(status_code=404, detail="Estudante não encontrado para vincular o perfil")

    # Verifica se o estudante já tem perfil (Regra 1:1)
    if db_estudante.perfil:
         raise HTTPException(status_code=400, detail="Este estudante já possui um perfil vinculado")

    db_perfil = models.Perfil(**perfil.model_dump())
    db.add(db_perfil)
    db.commit()
    db.refresh(db_perfil)
    return db_perfil

# --- ROTAS DE MATRÍCULAS ---

@app.post("/matriculas/", response_model=schemas.MatriculaResponse)
def create_matricula(matricula: schemas.MatriculaCreate, db: Session = Depends(get_db)):
    db_matricula = models.Matricula(**matricula.model_dump())
    db.add(db_matricula)
    db.commit()
    db.refresh(db_matricula)
    return db_matricula

@app.get("/matriculas/", response_model=List[schemas.MatriculaResponse])
def read_matriculas(db: Session = Depends(get_db)):
    return db.query(models.Matricula).all()