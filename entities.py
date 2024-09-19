from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from api_terminal.database import Base

class Pessoa(Base):
    __tablename__ = 'pessoas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)  # Tipo Date para data de nascimento
    cpf = Column(String(14), unique=True, nullable=False)
    enderecos = relationship("Endereco", back_populates="pessoa", cascade="all, delete-orphan")

    def __init__(self, nome: str, data_nascimento: Date, cpf: str):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __str__(self):
        data_nascimento_str = self.data_nascimento.strftime('%d/%m/%Y')  # Formatação direta da data
        return f'{self.nome} | {data_nascimento_str} | {self.cpf}'

class Endereco(Base):
    __tablename__ = 'enderecos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rua = Column(String(150), nullable=False)
    numero = Column(Integer, nullable=False)
    complemento = Column(String(20), nullable=True)
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(9), nullable=False)
    pessoa_id = Column(Integer, ForeignKey('pessoas.id'), nullable=False)
    pessoa = relationship("Pessoa", back_populates="enderecos")

    def __init__(self, rua: str, numero: int, complemento: str, bairro: str, cidade: str, estado: str, cep: str, pessoa_id: int):
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.pessoa_id = pessoa_id

    def __str__(self):
        return f'{self.rua} | {self.numero} | {self.complemento} | {self.bairro} | {self.cidade} | {self.estado} | {self.cep} | {self.pessoa_id}'

