from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from database_fast import get_db
from endereco_fast import cadastra_endereco, exibe_enderecos, exibe_endereco_por_id, atualiza_endereco, exclui_endereco
from entities import Endereco

app = FastAPI()

# Modelos de dados
class EnderecoBase(BaseModel):
    rua: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    estado: str
    cep: str
    pessoa_id: int

class EnderecoCreate(EnderecoBase):
    pass

class EnderecoUpdate(BaseModel):
    rua: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None

class EnderecoResponse(EnderecoBase):
    id: int

    class Config:
        from_attributes = True

@app.post("/enderecos/", response_model=EnderecoResponse)
def criar_endereco(endereco: EnderecoCreate, db: Session = Depends(get_db)):
    novo_endereco = cadastra_endereco(
        db,
        endereco.rua,
        endereco.numero,
        endereco.complemento,
        endereco.bairro,
        endereco.cidade,
        endereco.estado,
        endereco.cep,
        endereco.pessoa_id
    )
    if novo_endereco:
        return novo_endereco
    else:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar endereço")

@app.get("/enderecos/", response_model=List[EnderecoResponse])
def listar_enderecos(db: Session = Depends(get_db)):
    enderecos = exibe_enderecos(db)
    return [
        EnderecoResponse(
            id=e.id,
            rua=e.rua,
            numero=e.numero,
            complemento=e.complemento,
            bairro=e.bairro,
            cidade=e.cidade,
            estado=e.estado,
            cep=e.cep,
            pessoa_id=e.pessoa_id
        ) for e in enderecos
    ]

@app.get("/enderecos/{id}", response_model=EnderecoResponse)
def obter_endereco(id: int, db: Session = Depends(get_db)):
    endereco = exibe_endereco_por_id(db, id)
    if endereco is None:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return EnderecoResponse(
        id=endereco.id,
        rua=endereco.rua,
        numero=endereco.numero,
        complemento=endereco.complemento,
        bairro=endereco.bairro,
        cidade=endereco.cidade,
        estado=endereco.estado,
        cep=endereco.cep,
        pessoa_id=endereco.pessoa_id
    )

@app.put("/enderecos/{endereco_id}", response_model=EnderecoResponse)
def atualizar_endereco(endereco_id: int, endereco: EnderecoUpdate, db: Session = Depends(get_db)):
    endereco_atualizado = atualiza_endereco(
        db,
        endereco_id,
        rua=endereco.rua,
        numero=endereco.numero,
        complemento=endereco.complemento,
        bairro=endereco.bairro,
        cidade=endereco.cidade,
        estado=endereco.estado,
        cep=endereco.cep
    )
    if endereco_atualizado:
        return endereco_atualizado
    else:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")

@app.delete("/enderecos/{endereco_id}", response_model=EnderecoResponse)
def deletar_endereco(endereco_id: int, db: Session = Depends(get_db)):
    endereco_excluido = exclui_endereco(db, endereco_id)
    if endereco_excluido:
        return endereco_excluido
    else:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
