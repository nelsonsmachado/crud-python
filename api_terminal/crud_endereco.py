# from sqlalchemy.orm import joinedload
# from sqlalchemy.exc import SQLAlchemyError
# from utils import voltar_ao_menu_principal
# from entities import Endereco
# from database import get_db

# # Funções de validação
# def valida_rua(rua: str) -> str:
#     while not rua.strip():
#         print("O campo 'rua' é obrigatório. Por favor, insira uma rua válida.")
#         rua = input("Digite a rua: ").strip()
#     return rua.strip()

# def valida_numero(numero: str) -> int:
#     while not numero.strip().isdigit():
#         print("O campo 'número' é obrigatório e deve ser um número válido.")
#         numero = input("Digite o número: ").strip()
#     return int(numero.strip())

# def valida_cep(cep: str) -> str:
#     while not cep.strip():
#         print("O campo 'CEP' é obrigatório. Por favor, insira um CEP válido.")
#         cep = input("Digite o CEP: ").strip()
#     return cep.strip()

# def confirma_dados(rua: str, numero: int, complemento: str, bairro: str, cidade: str, estado: str, cep: str, pessoa_id: int) -> bool:
#     print(f'\nRua: {rua}')
#     print(f'Número: {numero}')
#     print(f'Complemento: {complemento}')
#     print(f'Bairro: {bairro}')
#     print(f'Cidade: {cidade}')
#     print(f'Estado: {estado}')
#     print(f'CEP: {cep}')
#     print(f'ID da Pessoa: {pessoa_id}')
#     confirmacao = input("Os dados estão corretos? (s/n): ").strip().lower()
#     return confirmacao == 's'

# # Função para cadastrar endereço
# def cadastra_endereco():
#     db = next(get_db())  # Obtém a sessão do banco de dados
#     try:
#         while True:
#             rua = valida_rua(input("Digite a rua: ").strip())
#             numero = valida_numero(input("Digite o número: ").strip())
#             complemento = input("Digite o complemento: ").strip()
#             bairro = input("Digite o bairro: ").strip()
#             cidade = input("Digite a cidade: ").strip()
#             estado = input("Digite o estado: ").strip()
#             cep = valida_cep(input("Digite o CEP: ").strip())
#             pessoa_id = int(input("Digite o ID da pessoa: ").strip())

#             if confirma_dados(rua, numero, complemento, bairro, cidade, estado, cep, pessoa_id):
#                 break  # Saia do loop se os dados forem confirmados

#         try:
#             novo_endereco = Endereco(
#                 rua=rua, numero=numero, complemento=complemento, bairro=bairro,
#                 cidade=cidade, estado=estado, cep=cep, pessoa_id=pessoa_id
#             )
#             db.add(novo_endereco)
#             db.commit()
#             db.refresh(novo_endereco)
#             print(f'Endereço cadastrado com sucesso.\n({novo_endereco})')
#         except SQLAlchemyError as e:
#             db.rollback()
#             print(f"Erro ao cadastrar endereço: {e}")
#     finally:
#         voltar_ao_menu_principal()

# # Função para exibir todos os endereços
# def exibe_enderecos():
#     db = next(get_db())  # Obtém a sessão do banco de dados
#     try:
#         enderecos = db.query(Endereco).options(joinedload(Endereco.pessoa)).all()
#         if not enderecos:
#             print("Nenhum endereço cadastrado.")
#             return enderecos

#         # Exibe cabeçalho
#         print(f"{'ID'.ljust(5)} | {'Rua'.ljust(35)} | {'Número'.ljust(6)} | {'Complemento'.ljust(15)} | {'Bairro'.ljust(20)} | {'Cidade'.ljust(25)} | {'Estado'.ljust(8)} | {'CEP'.ljust(10)} | {'ID Pessoa'}")
#         print("-" * 160)
#         for endereco in enderecos:
#             print(f"{str(endereco.id).ljust(5)} | {endereco.rua.ljust(35)} | {str(endereco.numero).ljust(6)} | {endereco.complemento.ljust(15)} | {endereco.bairro.ljust(20)} | {endereco.cidade.ljust(25)} | {endereco.estado.ljust(8)} | {endereco.cep.ljust(10)} | {str(endereco.pessoa_id)}")
#             print("*" * 160)
#             print('')
#         return enderecos
#     except SQLAlchemyError as e:
#         print(f"Erro ao listar endereços: {e}")
#         return []
#     finally:
#         voltar_ao_menu_principal()

# # Função para exibir endereço por ID
# def exibe_endereco_por_id(endereco_id: int):
#     db = next(get_db())  # Obtém a sessão do banco de dados
#     try:
#         endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
#         if endereco:
#             print(f"{str(endereco.id).ljust(5)} | {endereco.rua.ljust(35)} | {str(endereco.numero).ljust(6)} | {endereco.complemento.ljust(15)} | {endereco.bairro.ljust(20)} | {endereco.cidade.ljust(25)} | {endereco.estado.ljust(8)} | {endereco.cep.ljust(10)} | {str(endereco.pessoa_id)}")
#         else:
#             print(f"Endereço com ID {endereco_id} não encontrado.")
#         return endereco
#     except SQLAlchemyError as e:
#         print(f"Erro ao buscar endereço por ID: {e}")
#         return None
#     finally:
#         voltar_ao_menu_principal()

# # Função para atualizar endereço
# def atualiza_endereco(endereco_id: int):
#     db = next(get_db())  # Obtém a sessão do banco de dados
#     try:
#         endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
#         if endereco:
#             # Exibir os dados atuais do endereço
#             print(f"Dados atuais do endereço:")
#             print(f"ID: {endereco.id}")
#             print(f"Rua: {endereco.rua}")
#             print(f"Número: {endereco.numero}")
#             print(f"Complemento: {endereco.complemento}")
#             print(f"Bairro: {endereco.bairro}")
#             print(f"Cidade: {endereco.cidade}")
#             print(f"Estado: {endereco.estado}")
#             print(f"CEP: {endereco.cep}")
#             print(f"ID da Pessoa: {endereco.pessoa_id}")

#             # Solicitar novos dados
#             rua = input("Digite a nova rua (ou deixe em branco para manter a atual): ").strip()
#             numero = input("Digite o novo número (ou deixe em branco para manter o atual): ").strip()
#             complemento = input("Digite o novo complemento (ou deixe em branco para manter o atual): ").strip()
#             bairro = input("Digite o novo bairro (ou deixe em branco para manter o atual): ").strip()
#             cidade = input("Digite a nova cidade (ou deixe em branco para manter a atual): ").strip()
#             estado = input("Digite o novo estado (ou deixe em branco para manter o atual): ").strip()
#             cep = input("Digite o novo CEP (ou deixe em branco para manter o atual): ").strip()

#             # Atualizar os dados somente se o usuário fornecer novos valores
#             if rua:
#                 endereco.rua = rua
#             if numero:
#                 endereco.numero = int(numero)
#             if complemento:
#                 endereco.complemento = complemento
#             if bairro:
#                 endereco.bairro = bairro
#             if cidade:
#                 endereco.cidade = cidade
#             if estado:
#                 endereco.estado = estado
#             if cep:
#                 endereco.cep = cep

#             db.commit()
#             db.refresh(endereco)
#             print(f'Endereço atualizado com sucesso.\n({endereco})')
#         else:
#             print(f"Endereço com ID {endereco_id} não encontrado.")
#     except SQLAlchemyError as e:
#         db.rollback()
#         print(f"Erro ao atualizar endereço: {e}")
#     finally:
#         voltar_ao_menu_principal()

# # Função para deletar endereço
# def deleta_endereco(endereco_id: int):
#     db = next(get_db())  # Obtém a sessão do banco de dados
#     try:
#         endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
#         if endereco:
#             db.delete(endereco)
#             db.commit()
#             print(f'Endereço com ID {endereco_id} deletado com sucesso.')
#         else:
#             print(f"Endereço com ID {endereco_id} não encontrado.")
#     except SQLAlchemyError as e:
#         db.rollback()
#         print(f"Erro ao deletar endereço: {e}")
#     finally:
#         voltar_ao_menu_principal()
from sqlalchemy.exc import SQLAlchemyError
from api_terminal.utils import volta_ao_menu_principal
from entities import Endereco
from api_terminal.database import get_db

# Funções de validação
def valida_rua(rua: str) -> str:
    while not rua.strip():
        print("O campo 'rua' é obrigatório. Por favor, insira uma rua válida.")
        rua = input("Digite a rua: ").strip()
    return rua.strip()

def valida_numero(numero: str) -> str:
    while not numero.strip().isdigit():
        print("O campo 'número' é obrigatório e deve ser um número válido.")
        numero = input("Digite o número: ").strip()
    return numero.strip()

def confirma_dados(rua: str, numero: str, complemento: str, bairro: str, cidade: str, estado: str, cep: str, pessoa_id: int) -> bool:
    print(f'\nRua: {rua}')
    print(f'Número: {numero}')
    print(f'Complemento: {complemento}')
    print(f'Bairro: {bairro}')
    print(f'Cidade: {cidade}')
    print(f'Estado: {estado}')
    print(f'CEP: {cep}')
    print(f'Pessoa_ID: {pessoa_id}')
    confirmacao = input("Os dados estão corretos? (s/n): ").strip().lower()
    return confirmacao == 's'

# Função para cadastrar endereço
def cadastra_endereco(pessoa_id: int):
    with get_db() as db:
        try:
            while True:
                rua = valida_rua(input("Digite a rua: ").strip())
                numero = valida_numero(input("Digite o número: ").strip())
                complemento = input("Digite o complemento: ").strip()
                bairro = input("Digite o bairro: ").strip()
                cidade = input("Digite a cidade: ").strip()
                estado = input("Digite o estado: ").strip()
                cep = input("Digite o CEP: ").strip()
                pessoa_id = input("Digite o ID_Pessoa: ").strip()

                if confirma_dados(rua, numero, complemento, bairro, cidade, estado, cep, pessoa_id):
                    break  # Saia do loop se os dados forem confirmados

            try:
                novo_endereco = Endereco(rua=rua, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, estado=estado, cep=cep, pessoa_id=pessoa_id)
                db.add(novo_endereco)
                db.commit()
                db.refresh(novo_endereco)
                print(f'Endereço cadastrado com sucesso.\n({novo_endereco})')
            except SQLAlchemyError as e:
                db.rollback()
                print(f"Erro ao cadastrar endereço: {e}")
        finally:
            volta_ao_menu_principal()

# Função para exibir todos os endereços
def exibe_enderecos():
    with get_db() as db:
        try:
            # Consulta para retornar todos os endereços
            enderecos = db.query(Endereco).all()
            # Exibindo os resultados
            for endereco in enderecos:
                print(f"{'ID'.ljust(5)} | {'Rua'.ljust(35)} | {'Número'.ljust(6)} | {'Complemento'.ljust(10)} | {'Bairro'.ljust(20)} | {'Cidade'.ljust(25)} | {'Estado'.ljust(10)} | {'CEP'.ljust(10)} | {'ID Pessoa'}")
                print("-" * 160)
                print(f"{str(endereco.id).ljust(5)} | {endereco.rua.ljust(35)} | {str(endereco.numero).ljust(6)} | {endereco.complemento.ljust(10)} | {endereco.bairro.ljust(20)} | {endereco.cidade.ljust(25)} | {endereco.estado.ljust(10)} | {endereco.cep.ljust(10)} | {str(endereco.pessoa_id)}\n")
            return enderecos
        except SQLAlchemyError as e:
            print(f"Erro ao listar endereços: {e}")
            return []
        finally:
            db.close()
            volta_ao_menu_principal()

# Função para exibir endereço por ID
def exibe_endereco_por_id(endereco_id: int):
    with get_db() as db:
        try:
            endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
            if endereco:
                print(f"{'ID'.ljust(5)} | {'Rua'.ljust(35)} | {'Número'.ljust(6)} | {'Complemento'.ljust(12)} | {'Bairro'.ljust(20)} | {'Cidade'.ljust(25)} | {'Estado'.ljust(10)} | {'CEP'.ljust(10)} | {'ID Pessoa'}")
                print(f"{str(endereco.id).ljust(5)} | {endereco.rua.ljust(35)} | {str(endereco.numero).ljust(6)} | {endereco.complemento.ljust(12)} | {endereco.bairro.ljust(20)} | {endereco.cidade.ljust(25)} | {endereco.estado.ljust(10)} | {endereco.cep.ljust(10)} | {str(endereco.pessoa_id)}\n")
            else:
                print(f"Endereço com ID {endereco_id} não encontrado.")
            return endereco
        except SQLAlchemyError as e:
            print(f"Erro ao buscar endereço por ID: {e}")
            return None
        finally:
            volta_ao_menu_principal()

# Função para atualizar endereço
def atualiza_endereco(endereco_id: int):
    with get_db() as db:
        try:
            endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
            if endereco:
                # Exibir os dados atuais do endereço
                print(f"Dados atuais do endereço:")
                print(f"ID: {endereco.id}")
                print(f"Rua: {endereco.rua}")
                print(f"Número: {endereco.numero}")
                print(f"Complemento: {endereco.complemento}")
                print(f"Bairro: {endereco.bairro}")
                print(f"Cidade: {endereco.cidade}")
                print(f"Estado: {endereco.estado}")
                print(f"CEP: {endereco.cep}")
                print(f"Pessoa_ID: {endereco.pessoa_id}")

                # Solicitar novos dados
                rua = input("Digite a nova rua (ou deixe em branco para manter a atual): ").strip()
                numero = input("Digite o novo número (ou deixe em branco para manter o atual): ").strip()
                complemento = input("Digite o complento (ou deixe em branco para manter o atual): ").strip()
                bairro = input("Digite o novo bairro (ou deixe em branco para manter o atual): ").strip()
                cidade = input("Digite a nova cidade (ou deixe em branco para manter a atual): ").strip()
                estado = input("Digite o novo estado (ou deixe em branco para manter o atual): ").strip()
                cep = input("Digite o novo CEP (ou deixe em branco para manter o atual): ").strip()
                pessoa_id = input("Digite o novo ID (ou deixe em branco para manter o atual: ").strip()

                # Atualizar os dados somente se o usuário fornecer novos valores
                if rua:
                    endereco.rua = rua
                if numero:
                    endereco.numero = numero
                if complemento:
                    endereco.complemento = complemento
                if bairro:
                    endereco.bairro = bairro
                if cidade:
                    endereco.cidade = cidade
                if estado:
                    endereco.estado = estado
                if cep:
                    endereco.cep = cep
                if pessoa_id:
                    endereco.pessoa_id = pessoa_id

                db.commit()
                db.refresh(endereco)
                print(f'Endereço atualizado com sucesso.\n({endereco})')
            else:
                print(f"Endereço com ID {endereco_id} não encontrado.")
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao atualizar endereço: {e}")
        finally:
            volta_ao_menu_principal()

# Função para deletar endereço
def exclui_endereco(endereco_id: int):
    with get_db() as db:
        try:
            # Buscar o endereço pelo ID
            endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
            
            if endereco:
                # Exibir os dados do endereço para confirmação
                print(f"Dados do endereço a ser excluído:")
                print(f"ID: {endereco.id}")
                print(f"Rua: {endereco.rua}")
                print(f"Número: {endereco.numero}")
                print(f"Complemento: {endereco.complemento}")
                print(f"Bairro: {endereco.bairro}")
                print(f"Cidade: {endereco.cidade}")
                print(f"Estado: {endereco.estado}")
                print(f"CEP: {endereco.cep}")
                print(f"Pessoa_ID: {endereco.pessoa_id}")
                
                # Solicitar confirmação do usuário
                confirmacao = input("Você realmente deseja excluir este endereço? (s/n): ").strip().lower()
                
                if confirmacao == 's':
                    # Excluir o endereço e confirmar a exclusão
                    db.delete(endereco)
                    db.commit()
                    print(f"Endereço com ID {endereco_id} excluído com sucesso.")
                    volta_ao_menu_principal()
                    return endereco
                else:
                    print("Exclusão cancelada.")
                    volta_ao_menu_principal()
                    return None
            else:
                print(f"Endereço com ID {endereco_id} não encontrado.")
                volta_ao_menu_principal()
                return None
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao excluir endereço: {e}")
            return None
