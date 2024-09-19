from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from api_terminal.utils import volta_ao_menu_principal
from entities import Pessoa
from api_terminal.database import get_db

# Funções de validação
def valida_nome(nome: str) -> str:
    while not nome.strip():
        print("O campo 'nome' é obrigatório. Por favor, insira um nome válido.")
        nome = input("Digite o nome: ").strip()
    return nome.strip()

def valida_cpf(cpf: str) -> str:
    while not cpf.strip():
        print("O campo 'CPF' é obrigatório. Por favor, insira um CPF válido.")
        cpf = input("Digite o CPF: ").strip()
    return cpf.strip()

def confirma_dados(nome: str, data_nascimento: str, cpf: str) -> bool:
    print(f'\nNome: {nome}')
    print(f'Data de Nascimento: {data_nascimento}')
    print(f'CPF: {cpf}')
    confirmacao = input("Os dados estão corretos? (s/n): ").strip().lower()
    return confirmacao == 's'

# Função para cadastrar pessoa
def cadastra_pessoa():
    with get_db() as db:  # Obtém a sessão do banco de dados
        try:
            while True:
                nome = valida_nome(input("Digite o nome: ").strip())
                data_nascimento = input("Digite a data de nascimento (YYYY-MM-DD): ").strip()
                cpf = valida_cpf(input("Digite o CPF: ").strip())

                if confirma_dados(nome, data_nascimento, cpf):
                    break  # Saia do loop se os dados forem confirmados

            try:
                nova_pessoa = Pessoa(nome=nome, data_nascimento=data_nascimento, cpf=cpf)
                db.add(nova_pessoa)
                db.commit()
                db.refresh(nova_pessoa)
                print(f'Pessoa cadastrada com sucesso.\n({nova_pessoa})')
            except SQLAlchemyError as e:
                db.rollback()
                print(f"Erro ao cadastrar pessoa: {e}")
        finally:
            volta_ao_menu_principal()

# Função para exibir todas as pessoas
def exibe_pessoas():
    with get_db() as db:
        try:
            # Consulta para retornar todas as pessoas com seus endereços
            pessoas = db.query(Pessoa).options(joinedload(Pessoa.enderecos)).all()
            # Exibindo os resultados
            for pessoa in pessoas:
                print(f"{'ID'.ljust(5)} | {'Nome'.ljust(30)} | {'Data de Nascimento'.ljust(20)} | {'CPF'}")
                print("-" * 160)
                print(f"{str(pessoa.id).ljust(5)} | {pessoa.nome.ljust(30)} | {pessoa.data_nascimento.strftime('%d/%m/%Y').ljust(20)} | {pessoa.cpf}")

                # Exibe os endereços vinculados a cada pessoa
                if pessoa.enderecos:
                    print("\nEndereços:")
                    print(f"{'ID'.ljust(5)} | {'Rua'.ljust(35)} | {'Numero'.ljust(6)} | {'Complemento'.ljust(15)} | {'Bairro'.ljust(20)} | {'Cidade'.ljust(25)} | {'Estado'.ljust(8)} | {'CEP'.ljust(10)} | {'ID Pessoa'}")
                    for endereco in pessoa.enderecos:
                        print(f"{str(endereco.id).ljust(5)} | {endereco.rua.ljust(35)} | {str(endereco.numero).ljust(6)} | {endereco.complemento.ljust(15)} | {endereco.bairro.ljust(20)} | {endereco.cidade.ljust(25)} | {endereco.estado.ljust(8)} | {endereco.cep.ljust(10)} | {str(endereco.pessoa_id)}\n")
                        print("*" * 160)
                        print('')
                else:
                    print("\nSem endereços cadastrados.\n")
                    print("*" * 160)
                    print('')
            return pessoas
        except SQLAlchemyError as e:
            print(f"Erro ao listar pessoas: {e}")
            return []
        finally:
            db.close()
            volta_ao_menu_principal()

# Função para exibir pessoa por ID
def exibe_pessoa_por_id(pessoa_id: int):
    with get_db() as db:
        try:
            pessoa = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
            if pessoa:
                print(f"{'ID'.ljust(5)} | {'Nome'.ljust(30)} | {'Data de Nascimento'.ljust(20)} | {'CPF'}")
                print(f"{str(pessoa.id).ljust(5)} | {pessoa.nome.ljust(30)} | {pessoa.data_nascimento.strftime('%d/%m/%Y').ljust(20)} | {pessoa.cpf}")
                if pessoa.enderecos:
                    print("\nEndereços:")
                    for endereco in pessoa.enderecos:
                        print(f"{str(endereco.id).ljust(5)} | {endereco.rua.ljust(35)} | {str(endereco.numero).ljust(6)} | {endereco.complemento.ljust(15)} | {endereco.bairro.ljust(20)} | {endereco.cidade.ljust(25)} | {endereco.estado.ljust(8)} | {endereco.cep.ljust(10)} | {str(endereco.pessoa_id)}\n")
                else:
                    print("\nSem endereços cadastrados para esta pessoa.")
            else:
                print(f"Pessoa com ID {pessoa_id} não encontrada.")
            return pessoa
        except SQLAlchemyError as e:
            print(f"Erro ao buscar pessoa por ID: {e}")
            return None
        finally:
            volta_ao_menu_principal()

# Função para atualizar pessoa
def atualiza_pessoa(pessoa_id: int):
    with get_db() as db:  # Obtém a sessão do banco de dados
        try:
            pessoa = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
            if pessoa:
                # Exibir os dados atuais da pessoa
                print(f"Dados atuais da pessoa:")
                print(f"ID: {pessoa.id}")
                print(f"Nome: {pessoa.nome}")
                print(f"Data de Nascimento: {pessoa.data_nascimento}")
                print(f"CPF: {pessoa.cpf}")

                # Solicitar novos dados
                nome = input("Digite o novo nome (ou deixe em branco para manter o atual): ").strip()
                data_nascimento = input("Digite a nova data de nascimento (YYYY-MM-DD) (ou deixe em branco para manter a atual): ").strip()
                cpf = input("Digite o novo CPF (ou deixe em branco para manter o atual): ").strip()

                # Atualizar os dados somente se o usuário fornecer novos valores
                if nome:
                    pessoa.nome = nome
                if data_nascimento:
                    pessoa.data_nascimento = data_nascimento
                if cpf:
                    pessoa.cpf = cpf

                db.commit()
                db.refresh(pessoa)
                print(f'Pessoa atualizada com sucesso.\n({pessoa})')
            else:
                print(f"Pessoa com ID {pessoa_id} não encontrada.")
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao atualizar pessoa: {e}")
        finally:
            volta_ao_menu_principal()

# Função para deletar pessoa
def exclui_pessoa(pessoa_id: int):
    with get_db() as db:
        try:
            # Buscar a pessoa pelo ID
            pessoa = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
            
            if pessoa:
                # Exibir os dados da pessoa para confirmação
                print(f"Dados da pessoa a ser excluída:")
                print(f"ID: {pessoa.id}")
                print(f"Nome: {pessoa.nome}")
                print(f"Data de Nascimento: {pessoa.data_nascimento}")
                print(f"CPF: {pessoa.cpf}")
                
                # Solicitar confirmação do usuário
                confirmacao = input("Você realmente deseja excluir esta pessoa? (s/n): ").strip().lower()
                
                if confirmacao == 's':
                    # Excluir a pessoa e confirmar a exclusão
                    db.delete(pessoa)
                    db.commit()
                    print(f"Pessoa com ID {pessoa_id} excluída com sucesso.")
                    volta_ao_menu_principal()
                    return pessoa
                else:
                    print("Exclusão cancelada.")
                    volta_ao_menu_principal()
                    return None
            else:
                print(f"Pessoa com ID {pessoa_id} não encontrada.")
                volta_ao_menu_principal()
                return None
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao excluir pessoa: {e}")
            return None


