from pydantic import BaseModel

# --- ESTUDANTES ---

class EstudanteBase(BaseModel):
    nome: str
    idade: int

class EstudanteCreate(EstudanteBase):
    pass

class EstudanteResponse(EstudanteBase):
    id: int

    class Config:
        # Isso diz ao Pydantic: "Pode ler os dados direto do objeto do banco de dados (SQLAlchemy)"
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