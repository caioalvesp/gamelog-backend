from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from model import Base

class Jogo(Base):
  __tablename__ = 'jogo'

  id = Column('pk_jogo', Integer, primary_key=True)
  nome = Column(String(140), unique=True)
  plataforma = Column(String(50))
  capa_url = Column(String(300), nullable=True)
  data_lancamento = Column(String(20), nullable=True)
  desenvolvedora = Column(String(140), nullable=True)
  nota_critica = Column(Integer, nullable=True)

  usuario_associations = relationship(
    'UsuarioJogo', back_populates='jogo', cascade='all, delete-orphan'
  )

  def __init__(self, nome:str, plataforma:str, capa_url:str=None,
               data_lancamento:str=None, desenvolvedora:str=None, nota_critica:int=None):
    """
    Cria um jogo

    Arguments:
      nome: nome do jogo
      plataforma: plataforma em que possui o jogo
      capa_url: URL da capa do jogo, obtida da API externa (RAWG)
      data_lancamento: data de lançamento do jogo, obtida da API externa
      desenvolvedora: desenvolvedora do jogo, obtida da API externa
      nota_critica: nota da crítica (Metacritic), obtida da API externa
    """
    self.nome = nome
    self.plataforma = plataforma
    self.capa_url = capa_url
    self.data_lancamento = data_lancamento
    self.desenvolvedora = desenvolvedora
    self.nota_critica = nota_critica
