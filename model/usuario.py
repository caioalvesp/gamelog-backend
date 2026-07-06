from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from model import Base
from model.usuario_jogo import UsuarioJogo


class Usuario(Base):
    __tablename__ = 'usuario'

    id   = Column('pk_usuario', Integer, primary_key=True)
    nome = Column(String(140), nullable=False)

    jogo_associations = relationship(
        'UsuarioJogo', backref='usuario', cascade='all, delete-orphan'
    )
    jogos = association_proxy('jogo_associations', 'jogo')

    def __init__(self, nome: str):
        self.nome = nome

    def adiciona_jogo(self, jogo, zerado: bool = False, nota: int = None):
        self.jogo_associations.append(UsuarioJogo(jogo=jogo, zerado=zerado, nota=nota))

    def remove_jogo(self, jogo):
        associacao = self.busca_associacao(jogo.id)
        if associacao is not None:
            self.jogo_associations.remove(associacao)

    def busca_associacao(self, jogo_id: int):
        """Retorna o UsuarioJogo (com zerado/nota) para um jogo, ou None."""
        return next((a for a in self.jogo_associations if a.jogo_id == jogo_id), None)
