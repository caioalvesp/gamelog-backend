from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

class Jogo(Base):
  __tablename__ = 'jogo'

  id = Column('pk_jogo', Integer, primary_key=True)
  nome = Column(String(140), unique=True)
  plataforma = Column(String(50))
  zerado = Column(Boolean, default=False, nullable=False)
  nota = Column(Integer)

  def __init__(self, nome:str, plataforma:str, zerado:bool, nota:int):
    """
    Cria um jogo

    Arguments:
      nome: nome do jogo
      plataforma: plataforma em que possui o jogo
      zerado: indica se o player zerou ou não
      nota: nota de avaliação pessoal atribuída pelo player
    """
    self.nome = nome
    self.plataforma = plataforma
    self.zerado = zerado
    self.nota = nota
