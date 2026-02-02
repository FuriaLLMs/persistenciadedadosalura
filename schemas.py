from pydantic import BaseModel
from typing import Optional, List

# --- PERFIL ---
class PerfilBase(BaseModel):
    idade: int
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

# --- DISCIPLINAS (N:N) ---

class DisciplinaBase(BaseModel):
    nome: str

class DisciplinaCreate(DisciplinaBase):
    pass

class DisciplinaResponse(DisciplinaBase):
    id: int

    class Config:
        from_attributes = True

# --- ESTUDANTES ---

class EstudanteBase(BaseModel):
    nome: str
    idade: int

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