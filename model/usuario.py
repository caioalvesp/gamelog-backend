from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from model import Base

usuario_jogo = Table('usuario_jogo', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuario.pk_usuario'), primary_key=True),
    Column('jogo_id',    Integer, ForeignKey('jogo.pk_jogo'),    primary_key=True)
)

class Usuario(Base):
    __tablename__ = 'usuario'

    id   = Column('pk_usuario', Integer, primary_key=True)
    nome = Column(String(140), nullable=False)
    jogos = relationship('Jogo', secondary=usuario_jogo, backref='usuarios')

    def __init__(self, nome: str):
        self.nome = nome

    def adiciona_jogo(self, jogo):
        self.jogos.append(jogo)

    def remove_jogo(self, jogo):
        self.jogos.remove(jogo)
