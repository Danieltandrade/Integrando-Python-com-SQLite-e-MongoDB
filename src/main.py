"""
    Módulo: Integrando-Python-com-SQLite-e-MongoDB
    Curso: Python Development
    Instituição: DIO.me
    Instrutor: Juliana Mascarenhas
"""

import textwrap
from classes_config import Cliente
from classes_config import Conta
from classes_config import CriandoObjeto
from classes_config import ConexaoDancoDados
from sqlalchemy import select
from sqlalchemy.orm import Session

def menu():

    menu = """\n
    ================ MENU ================
    [1]\tCriar Cliente
    [2]\tCriar Conta
    [3]\tListar Clientes
    [4]\tListar Contas
    [5]\tLista de Contas por Cliente
    [0]\tSair
    => """
    return input(textwrap.dedent(menu))

def cadastrando_cliente(engine):
    """_summary_

    Args:
        engine (_type_): _description_
    """
    print("@@@ Cadastro de Cliente! @@@\n")

    # Iniciando cadastro com nome completo e cpf
    nome = input("Digite o nome do cliente: ")
    cpf = input("Digite somente os numeros do CPF do cliente: ")

    # Digitando o endereço
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # Chamando o método "criando_objeto_cliente" para criar o objeto cliente.
    cliente = CriandoObjeto(engine, nome, cpf, endereco)
    cliente.objeto_cliente()
    
    print("@@@ Cliente criado com sucesso! @@@\n")

def cadastrando_conta(engine, numero_conta):
    """_summary_

    Args:
        engine (_type_): _description_
        numero_conta (_type_): _description_
    """
    print("@@@ Cadastro de Conta! @@@\n")

    # Digitando cpf para buscar o cliente na base de dados.
    cpf = input("Digite somente os numeros do CPF do cliente: ")

    session = Session(engine)
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    resultado = session.execute(stmt)

    for result in resultado.scalars():
        id_tabela = result.id

    tipo_conta = "Conta Corrente"
    agencia = "0001"
    num_conta = numero_conta
    saldo_conta = 0.0

    conta = CriandoObjeto.objeto_conta(engine, tipo_conta, agencia, num_conta, saldo_conta, id_tabela)
    print(conta)
    
    print("@@@ Conta criada com sucesso! @@@\n")

def lista_clientes(engine):
    """_summary_

    Args:
        engine (_type_): _description_
    """
    session = Session(engine)

    stmt = select(Cliente)
    print("\n@@@ Listando clientes do Banco! @@@")
    for clientes in session.scalars(stmt):
        print(clientes)

def lista_contas(engine):
    """_summary_

    Args:
        engine (_type_): _description_
    """
    session = Session(engine)

    stmt = select(Conta)
    print("\n@@@ Listando contas de clientes no Banco! @@@")
    for contas in session.scalars(stmt):
        print(contas)

def contas_cliente(engine):
    """_summary_

    Args:
        engine (_type_): _description_
    """
    print("@@@ Lista de conta do cliente! @@@\n")

    # Digitando cpf para buscar o cliente na base de dados.
    cpf = input("Digite somente os numeros do CPF do cliente: ")

    session = Session(engine)
    
    stmt_join = (select(Cliente.id, Cliente.nome, Conta.tipo, Conta.agencia, Conta.num).join(Conta, Cliente.id == Conta.id_cliente).where(Cliente.cpf == cpf))
    
    resultados = session.execute(stmt_join).all()
    
    for resultados_contas_cliente in resultados:
        print(resultados_contas_cliente)
    

def main(engine, num_conta):
    """_summary_

    Args:
        engine (_type_): _description_
        num_conta (_type_): _description_
    """
    while True:
        opcao = menu()
        
        if opcao == "1":  # Chamada para criação de um novo cliente dentro do banco de dados.
            cadastrando_cliente(engine)

        elif opcao == "2":
            cadastrando_conta(engine, num_conta)
            num_conta += 1

        elif opcao == "3":
            lista_clientes(engine)

        elif opcao == "4":
            lista_contas(engine)

        elif opcao == "5":
            contas_cliente(engine)

        elif opcao == "0":  # Finalizando loop.
            break

        else:
            print("\n@@@ Opção inválida, por favor selecione novamente a opção desejada. @@@")


# Criando "engine" para conexão com banco de dados.
conexao_banco_dados = ConexaoDancoDados()
engine = conexao_banco_dados.criando_engine_db()

# Aqui são criadas as tabelas caso elas não existam.
criando_tabelas = ConexaoDancoDados()
criando_tabelas.metadata_create_all(engine)

# Variável com número inicial de conta.
num_conta = 1001

# Chamando a função para execução do loop de código.
main(engine, num_conta)