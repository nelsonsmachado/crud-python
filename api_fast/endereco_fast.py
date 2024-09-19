from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from entities import Endereco  # Certifique-se de que o modelo Endereco está definido em entities.py
from database_fast import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

# Funções de validação
def valida_rua(rua: str) -> str:
    if not rua.strip():
        raise ValueError("O campo 'rua' é obrigatório. Por favor, insira uma rua válida.")
    return rua.strip()

def valida_numero(numero: str) -> str:
    if not numero.strip():
        raise ValueError("O campo 'número' é obrigatório. Por favor, insira um número válido.")
    return numero.strip()

def valida_bairro(bairro: str) -> str:
    if not bairro.strip():
        raise ValueError("O campo 'bairro' é obrigatório. Por favor, insira um bairro válido.")
    return bairro.strip()

def valida_cidade(cidade: str) -> str:
    if not cidade.strip():
        raise ValueError("O campo 'cidade' é obrigatório. Por favor, insira uma cidade válida.")
    return cidade.strip()

def valida_estado(estado: str) -> str:
    if not estado.strip():
        raise ValueError("O campo 'estado' é obrigatório. Por favor, insira um estado válido.")
    return estado.strip()

def valida_cep(cep: str) -> str:
    if not cep.strip():
        raise ValueError("O campo 'CEP' é obrigatório. Por favor, insira um CEP válido.")
    return cep.strip()

# Função para cadastrar endereço
def cadastra_endereco(db: Session, rua: str, numero: str, complemento: Optional[str], bairro: str, cidade: str, estado: str, cep: str, pessoa_id: int) -> Optional[Endereco]:
    try:
        rua = valida_rua(rua)
        numero = valida_numero(numero)
        bairro = valida_bairro(bairro)
        cidade = valida_cidade(cidade)
        estado = valida_estado(estado)
        cep = valida_cep(cep)

        novo_endereco = Endereco(
            rua=rua, 
            numero=numero, 
            complemento=complemento, 
            bairro=bairro, 
            cidade=cidade, 
            estado=estado, 
            cep=cep,
            pessoa_id=pessoa_id
        )
        db.add(novo_endereco)
        db.commit()
        db.refresh(novo_endereco)
        return novo_endereco
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao cadastrar endereço: {e}")
        return None

# Função para exibir todos os endereços
def exibe_enderecos(db: Session) -> List[Endereco]:
    try:
        enderecos = db.query(Endereco).options(joinedload(Endereco.pessoa)).all()
        return enderecos
    except SQLAlchemyError as e:
        print(f"Erro ao listar endereços: {e}")
        return []

# Função para exibir endereço por ID
def exibe_endereco_por_id(db: Session, endereco_id: int) -> Optional[Endereco]:
    try:
        endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
        return endereco
    except SQLAlchemyError as e:
        print(f"Erro ao buscar endereço por ID: {e}")
        return None

# Função para atualizar endereço
def atualiza_endereco(db: Session, endereco_id: int, rua: Optional[str] = None, numero: Optional[str] = None, complemento: Optional[str] = None, bairro: Optional[str] = None, cidade: Optional[str] = None, estado: Optional[str] = None, cep: Optional[str] = None) -> Optional[Endereco]:
    try:
        endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
        if endereco:
            if rua:
                endereco.rua = valida_rua(rua)
            if numero:
                endereco.numero = valida_numero(numero)
            if complemento:
                endereco.complemento = complemento
            if bairro:
                endereco.bairro = valida_bairro(bairro)
            if cidade:
                endereco.cidade = valida_cidade(cidade)
            if estado:
                endereco.estado = valida_estado(estado)
            if cep:
                endereco.cep = valida_cep(cep)

            db.commit()
            db.refresh(endereco)
            return endereco
        else:
            return None
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao atualizar endereço: {e}")
        return None

# Função para deletar endereço
def exclui_endereco(db: Session, endereco_id: int) -> Optional[Endereco]:
    try:
        endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
        if endereco:
            db.delete(endereco)
            db.commit()
            return endereco
        else:
            return None
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao excluir endereço: {e}")
        return None

