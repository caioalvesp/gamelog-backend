from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship

from model import Base


class UsuarioJogo(Base):
    """Associação entre Usuario e Jogo: guarda o estado pessoal do usuário
    em relação a um jogo (se zerou e a nota que deu)."""
    __tablename__ = 'usuario_jogo'

    usuario_id = Column(Integer, ForeignKey('usuario.pk_usuario'), primary_key=True)
    jogo_id = Column(Integer, ForeignKey('jogo.pk_jogo'), primary_key=True)

    zerado = Column(Boolean, default=False, nullable=False)
    nota = Column(Integer, nullable=True)
    plataforma = Column(String(100), nullable=True)

    jogo = relationship('Jogo', back_populates='usuario_associations')

    def __init__(self, jogo, zerado: bool = False, nota: int = None, plataforma: str = None):
        self.jogo = jogo
        self.zerado = zerado
        self.nota = nota
        self.plataforma = plataforma
