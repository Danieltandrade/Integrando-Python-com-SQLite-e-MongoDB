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
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.orm import Session

def menu():
    """
    Função para criação do menu de escolha. Nesta função é utilizado o módulo "textwrap".
    
    Args:
        Nenhum
    
    Return: 
        str: Retorna uma lista com as opções do menu. 
    """

    menu = """\n
    ================ MENU ================
    [1]\tCriar Cliente
    [2]\tCriar Conta
    [3]\tListar Clientes
    [4]\tListar Contas
    [5]\tLista de Contas por Cliente
    [6]\tDeletar Cliente
    [0]\tSair
    => """

    return input(textwrap.dedent(menu))

def cadastrando_cliente(engine):
    """
    Função para cadastro de novos clientes.

    Args:
        engine (str): Recebe a variável "engine" da criação do banco de dados.
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
    """
    Função para cadastro de novas contas para o cliente.
    Cada conta deve ter um número diferente,
    
    Args:
        engine (str): Recebe a variável "engine" da criação do banco de dados.
        numero_conta (int): Recebe um número inteiro referente a conta do cliente.
    """

    print("@@@ Cadastro de Conta! @@@\n")

    # Digitando cpf para buscar o cliente na base de dados.
    cpf = input("Digite somente os numeros do CPF do cliente: ")

    # Criando a session para conversa com Banco de Dados.
    session = Session(engine)

    # Criando e executando o objeto da consulta pedida.
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    resultado = session.execute(stmt)

    # Processando e imprimindo os resultados.
    for result in resultado.scalars():
        id_tabela = result.id

    # Variáveis para cadastro na tabela "Conta"
    tipo_conta = "Conta Corrente"
    agencia = "0001"
    num_conta = numero_conta
    saldo_conta = 0.0

    conta = CriandoObjeto.objeto_conta(engine, tipo_conta, agencia, num_conta, saldo_conta, id_tabela)
    print(conta)

    # Fechando a session.
    session.close()
    
    print("@@@ Conta criada com sucesso! @@@\n")

def lista_clientes(engine):
    """
    Função que cria uma lista com todos os clientes cadastrados.

    Args:
        engine (str): Recebe a variável "engine" da criação do banco de dados.
    """

    # Criando a session para conversa com Banco de Dados.
    session = Session(engine)

    # Criando e executando o objeto da consulta pedida.
    stmt = select(Cliente)

    print("\n@@@ Listando clientes do Banco! @@@")
    
    # Processando e imprimindo os resultados.
    for clientes in session.scalars(stmt):
        print(clientes)

    # Fechando a session.
    session.close()

def lista_contas(engine):
    """
    Função que cria uma lista com todas as contas cadastradas.

    Args:
        engine (str): Recebe a variável "engine" da criação do banco de dados.
    """

    # Criando a session para conversa com Banco de Dados.
    session = Session(engine)

    # Criando e executando o objeto da consulta pedida.
    stmt = select(Conta)

    print("\n@@@ Listando contas de clientes no Banco! @@@")

    # Processando e imprimindo os resultados.
    for contas in session.scalars(stmt):
        print(contas)

    # Fechando a session.
    session.close()

def contas_cliente(engine):
    """
    Função que lista todas as contas cadastradas de um determinado cliente.
    É utilizado para filtragem o número de CPF do cliente.

    Args:
        engine (str): Recebe a variável "engine" da criação do banco de dados.
    """
    print("@@@ Lista de contas do cliente! @@@\n")

    # Digitando cpf para buscar o cliente na base de dados.
    cpf = input("Digite somente os numeros do CPF do cliente: ")

    session = Session(engine)

    # Consulta para selecionar os campos desejados.
    stmt_join = (select(Cliente.id, Cliente.nome, Conta.tipo, Conta.agencia, Conta.num).join(Conta, Cliente.id == Conta.id_cliente).where(Cliente.cpf == cpf))
    
    # Execute a consulta.
    resultados = session.execute(stmt_join).all()
    
    # Processar e imprimir os resultados.
    for resultados_contas_cliente in resultados:
        print(resultados_contas_cliente)

    # Fechando a session.
    session.close()

def delete_cliente(engine):
    """
    Função para deletar um cliente e suas contas associadas.

    Args:
        engine (str): Recebe a variável "engine" da criação do banco de dados.
    """

    print("\n@@@ Deletando Cliente e Conta! @@@\n")

    # Digitando cpf para buscar o cliente na base de dados.
    cpf = input("Digite somente os numeros do CPF do cliente: ")

    # Verifica se há certeza na exclusão do cliente.
    confirmacao = input("""
                        Deseja realmente excluir este cliente e conta?
                        Digite "s" para sim e "n" para não: 
                        """
                    )
    
    # Coloca o valor armazenado na variável em minúsculo
    confirmacao.lower()

    # Estrutura condicional para verificar se é ou não para excluir o cliente.
    if confirmacao == "s":

        # Criando a session para conversa com Banco de Dados.
        session = Session(engine)

        # Criando o objeto da consulta pedida.
        cliente = session.execute(select(Cliente).where(Cliente.cpf == cpf)).scalar_one_or_none()

        # Deletando o cliente (e automaticamente as contas associadas).
        session.delete(cliente)

        # Confirmando transação.
        session.commit()

        print(f"\n@@@ Cliente com CPF {cpf} e suas contas foram deletados. @@@\n")

        # Fechando a session.
        session.close()
    
    elif confirmacao == "n":
        print("\n@@@ Operação cancelada! @@@\n")
    
    else:
        print("\n@@@ Valor inválido. Operação cancelada! @@@\n")

def main(engine, numero_conta):
    """
    Função principal que executa um loop com as opções disponíveis.
    Para sair do loop é necessário digitar o número "0".

    Args:
        engine (str): Recebe a variável "engine" da criação do banco de dados.
        num_conta (int): Recebe um número inteiro inicial de conta, que é incrementado a cada novo cadastro de conta.
    """

    # Loop para execução dos menus existentes.
    while True:
        opcao = menu()
        
        if opcao == "1":  # Chamada para criação de um novo cliente dentro do banco de dados.
            cadastrando_cliente(engine)

        elif opcao == "2":
            cadastrando_conta(engine, numero_conta)
            numero_conta += 1

        elif opcao == "3":
            lista_clientes(engine)

        elif opcao == "4":
            lista_contas(engine)

        elif opcao == "5":
            contas_cliente(engine)
            
        elif opcao == "6":
            delete_cliente(engine)

        elif opcao == "0":  # Finalizando loop.
            break

        else:
            print("\n@@@ Opção inválida, por favor selecione novamente a opção desejada. @@@")


# Criando "engine" para conexão com banco de dados.
conexao_banco_dados = ConexaoDancoDados()
engine = conexao_banco_dados.criando_engine_db()

# Tabelas criadas caso elas não existam.
criando_tabelas = ConexaoDancoDados()
criando_tabelas.metadata_create_all(engine)

# Variável com número inicial de conta.
num_conta = 1001

# Chamando a função para execução do loop de código.
main(engine, num_conta)