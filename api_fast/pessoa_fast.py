from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from entities import Pessoa
from api_fast.database_fast import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

# Funções de validação
def valida_nome(nome: str) -> str:
    if not nome.strip():
        raise ValueError("O campo 'nome' é obrigatório. Por favor, insira um nome válido.")
    return nome.strip()

def valida_cpf(cpf: str) -> str:
    if not cpf.strip():
        raise ValueError("O campo 'CPF' é obrigatório. Por favor, insira um CPF válido.")
    return cpf.strip()

# Função para cadastrar pessoa
def cadastra_pessoa(db: Session, nome: str, data_nascimento: str, cpf: str) -> Optional[Pessoa]:
    try:
        nome = valida_nome(nome)
        cpf = valida_cpf(cpf)

        nova_pessoa = Pessoa(nome=nome, data_nascimento=data_nascimento, cpf=cpf)
        db.add(nova_pessoa)
        db.commit()
        db.refresh(nova_pessoa)
        return nova_pessoa
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao cadastrar pessoa: {e}")
        return None

# Função para exibir todas as pessoas
def exibe_pessoas(db: Session) -> List[Pessoa]:
    try:
        pessoas = db.query(Pessoa).options(joinedload(Pessoa.enderecos)).all()
        return pessoas
    except SQLAlchemyError as e:
        print(f"Erro ao listar pessoas: {e}")
        return []

# Função para exibir pessoa por ID
def exibe_pessoa_por_id(db: Session, pessoa_id: int) -> Optional[Pessoa]:
    try:
        pessoa = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
        return pessoa
    except SQLAlchemyError as e:
        print(f"Erro ao buscar pessoa por ID: {e}")
        return None

# Função para atualizar pessoa
def atualiza_pessoa(db: Session, pessoa_id: int, nome: Optional[str] = None, data_nascimento: Optional[str] = None, cpf: Optional[str] = None) -> Optional[Pessoa]:
    try:
        pessoa = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
        if pessoa:
            if nome:
                pessoa.nome = valida_nome(nome)
            if data_nascimento:
                pessoa.data_nascimento = data_nascimento
            if cpf:
                pessoa.cpf = valida_cpf(cpf)

            db.commit()
            db.refresh(pessoa)
            return pessoa
        else:
            return None
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao atualizar pessoa: {e}")
        return None

# Função para deletar pessoa
def exclui_pessoa(db: Session, pessoa_id: int) -> Optional[Pessoa]:
    try:
        pessoa = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
        if pessoa:
            db.delete(pessoa)
            db.commit()
            return pessoa
        else:
            return None
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao excluir pessoa: {e}")
        return None
