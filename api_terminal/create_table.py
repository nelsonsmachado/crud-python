from sqlalchemy.exc import SQLAlchemyError
from api_terminal.database import Base, engine
from entities import Pessoa, Endereco

def create_table():
    try:
        # Cria todas as tabelas definidas nas classes que herdam de Base
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso")
    except SQLAlchemyError as e:
        print("Erro na criação das tabelas:", str(e))

if __name__ == "__main__":
    create_table()

