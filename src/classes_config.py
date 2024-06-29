"""
    Módulo: Integrando-Python-com-SQLite-e-MongoDB
    Curso: Python Development
    Instituição: DIO.me
    Instrutor: Juliana Mascarenhas
    
    Arquivo com as classes que serão utilizadas pelo main.py para execução do código.
"""


from pprint import pprint
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from typing import List



class Base(DeclarativeBase):
    """
    Classe Base criada para novos mapeamentos declarativos.

    """
    pass


class Cliente(Base):
    """
    Classe que define a tabela "cliente"
    Nesta Classe está definido os atributos que serão usados na criação da tabela no Banco de Dados.

    Atributos:
        id (int): Identificador único do cliente.
        nome (str): Nome do cliente.
        cpf (str): CPF do cliente.
        endereco (str): Endereço do cliente.
        contas (List["Conta"]): Relacionamento com a tabela 'conta'.
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
            Engine: Instância do motor de banco de dados.
        """
        
        # Motor utilizado para criação do Banco de Dados.
        engine = create_engine(self.__string_de_conexao, echo=True)

        return engine

    def get_engine(self):
        """
        Método auxiliar para retorna o motor de banco de dados.

        Returns:
            Engine: Instância do motor de banco de dados.
        """
        
        return self.__engine
    
    def metadata_create_all(self, engine):
        """
        Método utilizado para criar as tabelas do Banco de Dados.

        Args:
            engine (Engine): Recebe motor do Banco de Dados.

        Returns:
            _type_: _description_
        """

        return Base.metadata.create_all(engine)


class ManipulandoMongoDB:
    """
    Classe para manipular o MongoDB.
    
    A Classe possui os métodos:
        -> connection_mongo_client()
        -> get_database_collection()
        -> inserindo_post_cliente()
        -> inserindo_post_conta()
    """
    
    def __init__(self):
        """
        Método construtor com atributos privados.
        """
        self.__client = None
        self.__db = None

    def connection_mongo_client(self):
        """
        Cria e retorna uma conexão com o MongoDB.

        Returns:
            MongoClient: Instância do cliente MongoDB.
        """

        client = MongoClient("mongodb+srv://danieltorresandrade:Padrao%2624F%2A@cluster0.p3wgir1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

        # Criando um Banco de Dados dentro do meu Cluster.
        self.__db = client.banco_dados
        
        return self.__db

    def inserindo_post_cliente(self, nome, cpf, endereco, db):
        """
        Insere um novo cliente no MongoDB.

        Args:
            nome (str): Nome do cliente.
            cpf (str): CPF do cliente.
            endereco (str): Endereço do cliente.
            db (Database): Instância do banco de dados MongoDB.
        """
        
        cliente = {
            "nome_cliente": nome,
            "cpf_cliente": cpf,
            "endereco_cliente": endereco,
        }
        
        clientes = db.clientes
        cliente_id = clientes.insert_one(cliente).inserted_id

        return clientes

    def inserino_post_conta(self, tipo, agencia, num, saldo, cpf, db):
        """
        Insere uma nova conta no MongoDB.

        Args:
            tipo (str): Tipo da conta.
            agencia (str): Agência da conta.
            num (int): Número da conta.
            saldo (float): Saldo da conta.
            cpf (str): CPF do cliente.
            db (Database): Instância do banco de dados MongoDB.
        """
        
        clientes = db.clientes
        
        conta_cliente = clientes.find_one({'cpf_cliente': cpf})
        
        conta = {
            "tipo_conta": tipo,
            "agencia": agencia,
            "numero_conta": num,
            "saldo_conta": saldo,
            "id_cliente": conta_cliente['_id']
        }

        contas = db.contas
        conta_id = contas.insert_one(conta).inserted_id
        
        return conta_id


class ListasMongoDB(ManipulandoMongoDB):
    """
        Classe para listar dados no MongoDB.

        Métodos:
            lista_clientes(db): Lista todos os clientes no MongoDB.
            lista_contas(db): Lista todas as contas no MongoDB.
            lista_cliente_e_conta(cpf, db): Lista um cliente e suas contas no MongoDB.
            deletando_cliente_e_contas(cpf, db): Deleta um cliente e suas contas no MongoDB.
    """

    def lista_clientes(self, db):
        """
        Lista todos os clientes no MongoDB.

        Args:
            db (Database): Instância do banco de dados MongoDB.
        """
        
        clientes = db.clientes
    
        for cliente in clientes.find():
            pprint(cliente)

    def lista_contas(self, db):
        """
        Lista todas as contas no MongoDB.

        Args:
            db (Database): Instância do banco de dados MongoDB.
        """
        
        contas = db.contas
    
        for conta in contas.find():
            pprint(conta)

    def lista_cliente_e_conta(self, cpf, db):
        """
        Lista um cliente e suas contas no MongoDB.

        Args:
            cpf (str): CPF do cliente.
            db (Database): Instância do banco de dados MongoDB.
        """
        
        clientes = db.clientes
        contas = db.contas

        cliente_filtrado = clientes.find_one({'cpf_cliente': cpf})

        print("\n@@@ Lista com cliente solicitado e suas respectivas contas. @@@")
        print(f"Cliente: {cliente_filtrado}")
        
        for contas_filtradas in contas.find({'id_cliente': cliente_filtrado['_id']}):
            print(f"\nContas: {contas_filtradas}")

    def deletando_cliente_e_contas(self, cpf, db):
        """
        Deleta um cliente e suas contas no MongoDB.

        Args:
            cpf (str): CPF do cliente.
            db (Database): Instância do banco de dados MongoDB.
        """
        
        clientes = db.clientes
        contas = db.contas
        
        cliente_filtrado = clientes.find_one({'cpf_cliente': cpf})
        
        deletando_contas = contas.delete_many({'id_cliente': cliente_filtrado['_id']})
        deletando_cliente = clientes.delete_one({'cpf_cliente': cpf})
