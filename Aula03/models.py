from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

#mysql
# engine = create_engine('mysql+pymysql://root:root@localhost:3306/pw2', echo=True)

engine = create_engine('sqlite:///example.db', echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,  primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(30), nullable=False)

class Produtos(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False)
    descricao = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    cpf = Column(String(11), nullable=False)
    nome = Column(String(100 ), nullable=False)
    endereco = Column(String(200), nullable=False)
    telefone = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)