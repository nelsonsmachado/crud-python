from datetime import date
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from api_fast.database_fast import get_db
from api_fast.pessoa_fast import cadastra_pessoa, exibe_pessoas, exibe_pessoa_por_id, atualiza_pessoa, exclui_pessoa
from entities import Pessoa

app = FastAPI()

# Modelos de dados
class PessoaBase(BaseModel):
    nome: str
    data_nascimento: str
    cpf: str

class PessoaCreate(PessoaBase):
    pass

class PessoaUpdate(BaseModel):
    nome: Optional[str]
    data_nascimento: Optional[str]
    cpf: Optional[str]

class PessoaResponse(PessoaBase):
    id: int

    class Config:
        from_attributes = True

def format_data_nascimento(data_nascimento: date) -> str:
    return data_nascimento.strftime('%Y-%m-%d')  # Ajuste o formato conforme necessário

@app.post("/pessoas/", response_model=PessoaResponse)
def criar_pessoa(pessoa: PessoaCreate, db: Session = Depends(get_db)):
    nova_pessoa = cadastra_pessoa(db, pessoa.nome, pessoa.data_nascimento, pessoa.cpf)
    if nova_pessoa:
        return nova_pessoa
    else:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar pessoa")

@app.get("/pessoas/", response_model=List[PessoaResponse])
def listar_pessoas(db: Session = Depends(get_db)):
    pessoas = exibe_pessoas(db)
    return [
        PessoaResponse(
            id=p.id,
            nome=p.nome,
            data_nascimento=format_data_nascimento(p.data_nascimento),
            cpf=p.cpf
        ) for p in pessoas
    ]

@app.get("/pessoas/{id}", response_model=PessoaResponse)
def obter_pessoa(id: int, db: Session = Depends(get_db)):
    pessoa = db.query(Pessoa).filter(Pessoa.id == id).first()
    if pessoa is None:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return PessoaResponse(
        id=pessoa.id,
        nome=pessoa.nome,
        data_nascimento=format_data_nascimento(pessoa.data_nascimento),
        cpf=pessoa.cpf
    )

@app.put("/pessoas/{pessoa_id}", response_model=PessoaResponse)
def atualizar_pessoa(pessoa_id: int, pessoa: PessoaUpdate, db: Session = Depends(get_db)):
    pessoa_atualizada = atualiza_pessoa(db, pessoa_id, nome=pessoa.nome, data_nascimento=pessoa.data_nascimento, cpf=pessoa.cpf)
    if pessoa_atualizada:
        return pessoa_atualizada
    else:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")

@app.delete("/pessoas/{pessoa_id}", response_model=PessoaResponse)
def deletar_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    pessoa_excluida = exclui_pessoa(db, pessoa_id)
    if pessoa_excluida:
        return pessoa_excluida
    else:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
