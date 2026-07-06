from sqlalchemy import Column, String, Integer

from model import Base

class Jogo(Base):
  __tablename__ = 'jogo'

  id = Column('pk_jogo', Integer, primary_key=True)
  nome = Column(String(140), unique=True)
  plataforma = Column(String(50))

  def __init__(self, nome:str, plataforma:str):
    """
    Cria um jogo

    Arguments:
      nome: nome do jogo
      plataforma: plataforma em que possui o jogo
    """
    self.nome = nome
    self.plataforma = plataforma
