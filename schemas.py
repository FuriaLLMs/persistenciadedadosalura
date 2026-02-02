from pydantic import BaseModel, EmailStr, PositiveInt
from typing import Optional, List

# --- PROFESSORES ---
class ProfessorBase(BaseModel):
    nome: str

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorResponse(ProfessorBase):
    id: int
    
    class Config:
        from_attributes = True

# --- DISCIPLINAS (N:N + Professor) ---

class DisciplinaBase(BaseModel):
    nome: str

class DisciplinaCreate(DisciplinaBase):
    professor_id: Optional[int] = None

class DisciplinaResponse(DisciplinaBase):
    id: int
    professor: Optional[ProfessorResponse] = None

    class Config:
        from_attributes = True

# --- PERFIL ---
class PerfilBase(BaseModel):
    idade: PositiveInt
    endereco: str

class PerfilCreate(PerfilBase):
    estudante_id: int

class PerfilResponse(PerfilBase):
    id: int
    estudante_id: int

    class Config:
        from_attributes = True

# --- MATRÍCULAS ---

class MatriculaBase(BaseModel):
    estudante_id: int
    nome_disciplina: str

class MatriculaCreate(MatriculaBase):
    pass

class MatriculaResponse(MatriculaBase):
    id: int

    class Config:
        from_attributes = True

# --- ESTUDANTES ---

class EstudanteBase(BaseModel):
    nome: str
    idade: PositiveInt
    email: EmailStr

class EstudanteCreate(EstudanteBase):
    pass

class EstudanteResponse(EstudanteBase):
    id: int
    perfil: Optional[PerfilResponse] = None
    matriculas: List[MatriculaResponse] = []
    disciplinas: List[DisciplinaResponse] = []

    class Config:
        # Isso diz ao Pydantic: "Pode ler os dados direto do objeto do banco de dados (SQLAlchemy)"
        from_attributes = True 