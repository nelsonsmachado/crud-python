import os
from datetime import datetime

def exibir_menu_opcoes():
    print("\nCadastro Imobiliário - Menu de opções: \n")
    print('1.  Cadastrar Cliente')
    print('2.  Exibir Cadastro de Clientes')
    print('3.  Exibir Cliente por ID')
    print('4.  Modificar Dados do Cliente no Cadastro')
    print('5.  Excluir Cliente do Cadastro')
    print('6.  Cadastrar Endereço')
    print('7.  Exibir Endereços')
    print('8.  Exibir Endereço por ID')
    print('9.  Atualizar Endereço')
    print('10. Excluir Endereço')
    print('11. Calculo de idade')
    print('0.  Sair\n')

def escolher_opcao():
    try:
        opcao_escolhida = int(input('Digite o número da opção escolhida: '))
        print()
        
        if opcao_escolhida == 1:
            from api_terminal.crud_pessoa import cadastra_pessoa
            cadastra_pessoa()
            
        elif opcao_escolhida == 2:
            from api_terminal.crud_pessoa import exibe_pessoas
            exibe_pessoas()
            
        elif opcao_escolhida == 3:
            from api_terminal.crud_pessoa import exibe_pessoa_por_id
            pessoa_id = int(input("Digite o ID da pessoa que deseja exibir: "))
            exibe_pessoa_por_id(pessoa_id)
                
        elif opcao_escolhida == 4:
            from api_terminal.crud_pessoa import atualiza_pessoa
            pessoa_id = int(input("Digite o ID da pessoa que deseja atualizar: "))
            atualiza_pessoa(pessoa_id)
                
        elif opcao_escolhida == 5:
            from api_terminal.crud_pessoa import exclui_pessoa
            pessoa_id = int(input("Digite o ID da pessoa que deseja excluir: "))
            exclui_pessoa(pessoa_id)
                
        elif opcao_escolhida == 6:
            from api_terminal.crud_endereco import cadastra_endereco
            pessoa_id = int(input("Digite o ID da pessoa que deseja vincular ao endereço: "))
            cadastra_endereco(pessoa_id)
            
        elif opcao_escolhida == 7:
            from api_terminal.crud_endereco import exibe_enderecos
            exibe_enderecos()
            
        elif opcao_escolhida == 8:
            from api_terminal.crud_endereco import exibe_endereco_por_id
            endereco_id = int(input("Digite o ID do endereço que deseja exibir: "))
            exibe_endereco_por_id(endereco_id)
                
        elif opcao_escolhida == 9:
            from api_terminal.crud_endereco import atualiza_endereco
            endereco_id = int(input("Digite o ID do endereço que deseja atualizar: "))
            atualiza_endereco(endereco_id)

        elif opcao_escolhida == 10:
            from api_terminal.crud_endereco import exclui_endereco
            endereco_id = int(input("Digite o ID do endereço que deseja excluir: "))
            exclui_endereco(endereco_id)
        
        elif opcao_escolhida == 11:
            calcula_idade()
                
        elif opcao_escolhida == 0:
            finaliza_api()
            
        else:
            opcao_invalida()
            
    except ValueError:
        print("Entrada inválida. Por favor, insira um número válido.")
        volta_ao_menu_principal()

def finaliza_api():
    print("Saindo do sistema...")
    print('Sistema encerrado. Até a próxima!')
    exit()

def opcao_invalida():
    print("Opção Inválida")
    volta_ao_menu_principal()

def volta_ao_menu_principal():
    input("Digite uma tecla qualquer para voltar ao menu principal.")
    exibir_menu_opcoes()
    escolher_opcao()

def inicia_api():
    os.system('cls')
    exibir_menu_opcoes()
    escolher_opcao()

def calcula_idade():
    data_atual = datetime.now()
    data_formatada = data_atual.strftime("%d/%m/%Y")
    data_nascimento_str = input("Informe aqui a sua data de nascimento (dd/mm/aaaa): ")
    data_nascimento = datetime.strptime(data_nascimento_str, "%d/%m/%Y")
    idade = data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))
    print(f"De acordo com sua data de nascimento({data_nascimento_str}), sua idade nesta data ({data_formatada}) é de {idade} anos.")
    volta_ao_menu_principal()

