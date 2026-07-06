from pydantic import BaseModel
from typing import List, Optional
from model.usuario import Usuario


class UsuarioSchema(BaseModel):
    """Define como um novo usuário a ser inserido deve ser representado"""
    nome: str = "Caio"

class UsuarioBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca por usuário"""
    id: int = 1

class UsuarioJogoSchema(BaseModel):
    """Define como deve ser a estrutura para desassociar um jogo de um usuário"""
    usuario_id: int = 1
    jogo_id: int = 1

class UsuarioJogoAddSchema(BaseModel):
    """Define como deve ser a estrutura para associar um jogo a um usuário,
    informando opcionalmente se já foi zerado e a nota dada pelo usuário"""
    usuario_id: int = 1
    jogo_id: int = 1
    zerado: Optional[bool] = False
    nota: Optional[int] = None

class UsuarioJogoUpdateSchema(BaseModel):
    """Define como deve ser a estrutura para atualizar o zerado/nota de um jogo
    já presente na coleção do usuário. Campos omitidos (None) não são alterados"""
    usuario_id: int = 1
    jogo_id: int = 1
    zerado: Optional[bool] = None
    nota: Optional[int] = None

class UsuarioViewSchema(BaseModel):
    """Define como um usuário será retornado"""
    id: int = 1
    nome: str = "Caio"
    jogos: list = []

class ListagemUsuariosSchema(BaseModel):
    """Define como uma listagem de usuários será retornada"""
    usuarios: List[UsuarioViewSchema]

class UsuarioDelSchema(BaseModel):
    """Define como deve ser a estrutura do dado retornado após uma requisição de remoção"""
    message: str
    id: int
    nome: str

def apresenta_usuario(usuario: Usuario):
    """Retorna uma representação do usuário seguindo o schema definido em UsuarioViewSchema"""
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "jogos": [
            {
                "id": assoc.jogo.id,
                "nome": assoc.jogo.nome,
                "plataforma": assoc.jogo.plataforma,
                "zerado": assoc.zerado,
                "nota": assoc.nota,
            }
            for assoc in usuario.jogo_associations
        ]
    }

def apresenta_usuarios(usuarios: List[Usuario]):
    """Retorna uma representação da listagem de usuários"""
    return {"usuarios": [apresenta_usuario(usuario) for usuario in usuarios]}
