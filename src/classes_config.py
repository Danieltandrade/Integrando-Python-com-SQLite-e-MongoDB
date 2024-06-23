"""
    Módulo: Integrando-Python-com-SQLite-e-MongoDB
    Curso: Python Development
    Instituição: DIO.me
    Instrutor: Juliana Mascarenhas
"""

from typing import List
from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    """
    Classe Base criada para novos mapeamentos declarativos.

    Args:
        DeclarativeBase (Class): Classe mãe usada para declarar definições da Classe Base.

    Returns:
        Any: Mapeamento declarativo.
    """


class Cliente(Base):
    """
    Classe com parâmetros para criação da tabela "cliente"
    Nesta Classe está definido os atributos que serão usados na criação da tabela no Banco de Dados.

    Args:
        Base (Class): Classe mãe com métodos para configuração da classe filha "Cliente".

    Returns:
        Tuple: Retorna uma tupla com as colunas da tabela.
    """

    # Definindo o nome da tabela para "cliente".
    __tablename__ = "cliente"

    # Atributos
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String)
    cpf: Mapped[str] = mapped_column(String(11))
    endereco: Mapped[str] = mapped_column(String(100))

    # Atributo utilizado para relacionar a tabela "Cliente" com a tabela "Conta"
    contas: Mapped[List["Conta"]] = relationship(back_populates="clientes", cascade="all, delete-orphan")

    # Método utilizado para realizar uma representação na forma de string da tabela.
    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"


class Conta(Base):
    """
    Classe com parâmetros para criação da tabela "conta"
    Nesta Classe está definido os atributos que serão usados na criação da tabela no Banco de Dados.

    Args:
        Base (Class): Classe mãe com métodos para configuração da classe filha "Conta".

    Returns:
        Tuple: Retorna uma tupla com as colunas da tabela.
    """

    # Definindo o nome da tabela para "conta".
    __tablename__ = "conta"

    # Atributos
    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String, default='conta corrente')
    agencia: Mapped[str] = mapped_column(String)
    num: Mapped[int]
    saldo: Mapped[float]
    id_cliente: Mapped[int] = mapped_column(ForeignKey("cliente.id"))

    # Atributo utilizado para relacionar a tabela "Conta" com a tabela "Cliente"
    clientes: Mapped["Cliente"] = relationship(back_populates="contas")

    # Método utilizado para realizar uma representação na forma de string da tabela.
    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, saldo={self.saldo})"


class CriandoObjeto:
    """
    Classe utilizada para criar os objetos cliente e conta.

    A Classe possui os métodos:
        -> objeto_cliente()
        -> objeto_conta()
    """
    def __init__(self, engine, nome_cliente, cpf_cliente, endereco_cliente):
        """
        Método construtor para instanciar os parâmetros da Classe.

        Args:
            engine (str): Recebe "engine" que foi utilizado para criação do Banco de Dados.
            nome_cliente (str): Recebe uma string com o nome do cliente.
            cpf_cliente (str): Recebe uma string com o cpf do cliente.
            endereco_cliente (str): Recebe uma string com o endereço do cliente.
        """

        self.engine = engine
        self.nome_cliente = nome_cliente
        self.cpf_cliente = cpf_cliente
        self.endereco_cliente = endereco_cliente
        
    def objeto_cliente(self):
        """
        Método criado para gravar no Banco de Dados o novo cliente.
        """
        
        # Chamando a Classe Session para adicionar o novo cliente.
        with Session(self.engine) as session:

            cliente = Cliente(
                nome = self.nome_cliente,
                cpf = self.cpf_cliente,
                endereco = self.endereco_cliente,
            )

        # Método chamado para adicionar um novo cliente.
        session.add(cliente)

        # Commit para adicionar o novo cliente.
        session.commit()

    def objeto_conta(self, tipo_conta, agencia_cliente, num_conta, saldo_conta, id_tabela_cliente):
        """
        Método criado para gravar no Banco de Dados a nova conta do cliente.

        Args:
            tipo_conta (str): Recebe uma string com o tipo de conta do cliente.
            agencia_cliente (str): Recebe uma string com a agencia do cliente.
            num_conta (int): Recebe um número inteiro referente a conta do cliente.
            saldo_conta (float): Recebe um número de ponto flutuante com o saldo da conta do cliente.
            id_tabela_cliente (int): Recebe "id" relacionado ao "id" da tabela cliente.
        """

        # Chamando a Classe Session para adicionar uma nova conta.
        with Session(self.engine) as session:

            conta = Conta(
                tipo = tipo_conta,
                agencia = agencia_cliente,
                num = num_conta,
                saldo = saldo_conta,
                id_cliente = id_tabela_cliente
            )

        # Método chamado para adiciona uma nova conta.
        session.add(conta)

        # Commit para adicionar a nova conta.
        session.commit()


class ConexaoDancoDados:
    """
    Classe para criar conexão com Banco de Dados.
    
    A Classe possui os métodos:
        -> criando_engine_db()
        -> get_engine()
        -> metadata_create_all()
    """
    def __init__(self):
        """
        Método construtor para instanciar os parâmetros da Classe.
        
        Args:
            __string_de_conexao (str): Argumento privado que recebe uma string.
            __engine (Engine): Argumento privado que recebe o método criando_engine_db()
        """
        self.__string_de_conexao = "sqlite://"
        self.__engine = self.criando_engine_db()

    def criando_engine_db(self):
        """
        Método criado para criar a conexão com o Banco de Dados.

        Returns:
            func: Retorna uma instância com o argumento para criação do Banco de Dados.
        """
        
        # Motor utilizado para criação do Banco de Dados.
        engine = create_engine(self.__string_de_conexao, echo=True)

        return engine

    def get_engine(self):
        """
        Método auxiliar para chamar diretamente a função create_engine.

        Returns:
            func: Retorna uma instância com o argumento para criação do Banco de Dados.
        """
        
        return self.__engine
    
    def metadata_create_all(self, engine):
        """
        Método utilizado para criar as tabelas do Banco de Dados caso elas não estejam criadas.

        Args:
            engine (str): Recebe "engine" que foi utilizado para criação do Banco de Dados.

        Returns:
            _type_: _description_
        """

        return Base.metadata.create_all(engine)
