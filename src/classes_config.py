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
    'Declarando a base de dados.'


class Cliente(Base):
    'Classe para inclusão de dados do cliente.'
    __tablename__ = "cliente"

    # Atributos
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String)
    cpf: Mapped[str] = mapped_column(String(11))
    endereco: Mapped[str] = mapped_column(String(100))

    contas: Mapped[List["Conta"]] = relationship(back_populates="clientes", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"


class Conta(Base):
    'Classe para inclusão de dados de conta.'
    __tablename__ = "conta"

    # Atributos
    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String, default='conta corrente')
    agencia: Mapped[str] = mapped_column(String)
    num: Mapped[int]
    saldo: Mapped[float]
    id_cliente: Mapped[int] = mapped_column(ForeignKey("cliente.id"))

    clientes: Mapped["Cliente"] = relationship(back_populates="contas")

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, saldo={self.saldo})"


class CriandoObjeto:
    'Classe para inclusão dos objetos: cliente e conta.'
    def __init__(self, engine, nome_cliente, cpf_cliente, endereco_cliente):
        self.engine = engine
        self.nome_cliente = nome_cliente
        self.cpf_cliente = cpf_cliente
        self.endereco_cliente = endereco_cliente
        
    def objeto_cliente(self):
        with Session(self.engine) as session:

            cliente = Cliente(
                nome = self.nome_cliente,
                cpf = self.cpf_cliente,
                endereco = self.endereco_cliente,
            )

        session.add(cliente)

        session.commit()

    def objeto_conta(self, tipo_conta, agencia_cliente, num_conta, saldo_conta, id_tabela_cliente):

        with Session(self.engine) as session:

            conta = Conta(
                tipo = tipo_conta,
                agencia = agencia_cliente,
                num = num_conta,
                saldo = saldo_conta,
                id_cliente = id_tabela_cliente
            )

        session.add(conta)

        session.commit()


class ConexaoDancoDados:
    """Criando conexão com Banco de Dados
    """
    def __init__(self):
        self.__string_de_conexao = "sqlite://"
        self.__engine = self.criando_engine_db()

    def criando_engine_db(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        engine = create_engine(self.__string_de_conexao, echo=True)
        return engine

    def get_engine(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__engine
    
    def metadata_create_all(self, engine):
        """_summary_

        Args:
            engine (_type_): _description_

        Returns:
            _type_: _description_
        """
        return Base.metadata.create_all(engine)
