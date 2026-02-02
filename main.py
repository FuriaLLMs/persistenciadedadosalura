from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
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
    try:
        # Converte o Pydantic (JSON) para o Modelo do Banco (SQLAlchemy)
        db_student = models.Estudante(**student.model_dump())
        
        db.add(db_student)      # Adiciona na "fila" do banco
        db.commit()             # Confirma a gravação (Salva de verdade)
        db.refresh(db_student)  # Atualiza o objeto com o ID gerado pelo banco
        
        return db_student
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Já existe um estudante com este email.")

# 2. GET: Listar Estudantes
# OTIMIZAÇÃO: joinedload para Perfil evita N+1 queries
@app.get("/estudantes/", response_model=List[schemas.EstudanteResponse])
def read_students(db: Session = Depends(get_db)):
    # SELECT * FROM estudantes LEFT JOIN perfis ON ...
    students = db.query(models.Estudante).options(joinedload(models.Estudante.perfil)).all()
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

# --- ROTAS DE PROFESSORES ---

@app.post("/professores/", response_model=schemas.ProfessorResponse)
def create_professor(professor: schemas.ProfessorCreate, db: Session = Depends(get_db)):
    db_professor = models.Professor(**professor.model_dump())
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

@app.get("/professores/", response_model=List[schemas.ProfessorResponse])
def read_professores(db: Session = Depends(get_db)):
    return db.query(models.Professor).all()

# --- ROTAS DE DISCIPLINAS (N:N) ---

@app.post("/disciplinas/", response_model=schemas.DisciplinaResponse)
def create_disciplina(disciplina: schemas.DisciplinaCreate, db: Session = Depends(get_db)):
    # Se houver professor_id, verificar se existe
    if disciplina.professor_id:
        db_professor = db.query(models.Professor).filter(models.Professor.id == disciplina.professor_id).first()
        if not db_professor:
             raise HTTPException(status_code=404, detail="Professor não encontrado")

    db_disciplina = models.Disciplina(**disciplina.model_dump())
    db.add(db_disciplina)
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina

@app.get("/disciplinas/", response_model=List[schemas.DisciplinaResponse])
def read_disciplinas(db: Session = Depends(get_db)):
    # Otimização: Carregar professor junto
    return db.query(models.Disciplina).options(joinedload(models.Disciplina.professor)).all()

# Endpoint para Matricular Estudante em Disciplina (Associação N:N)
@app.post("/estudantes/{estudante_id}/inscrever/{disciplina_id}", status_code=status.HTTP_200_OK)
def inscrever_estudante(estudante_id: int, disciplina_id: int, db: Session = Depends(get_db)):
    # 1. Buscar Estudante
    db_estudante = db.query(models.Estudante).filter(models.Estudante.id == estudante_id).first()
    if not db_estudante:
        raise HTTPException(status_code=404, detail="Estudante não encontrado")

    # 2. Buscar Disciplina
    db_disciplina = db.query(models.Disciplina).filter(models.Disciplina.id == disciplina_id).first()
    if not db_disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    # 3. Realizar a associação
    if db_disciplina not in db_estudante.disciplinas:
        db_estudante.disciplinas.append(db_disciplina)
        db.commit()
        return {"message": "Estudante inscrito com sucesso!"}
    
    return {"message": "Estudante já estava inscrito nesta disciplina."}