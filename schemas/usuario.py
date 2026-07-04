from pydantic import BaseModel
from typing import List
from model.usuario import Usuario


class UsuarioSchema(BaseModel):
    """Define como um novo usuário a ser inserido deve ser representado"""
    nome: str = "Caio"

class UsuarioBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca por usuário"""
    id: int = 1

class UsuarioJogoSchema(BaseModel):
    """Define como deve ser a estrutura para associar/desassociar um jogo a um usuário"""
    usuario_id: int = 1
    jogo_id: int = 1

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
        "jogos": [{"id": j.id, "nome": j.nome, "plataforma": j.plataforma} for j in usuario.jogos]
    }

def apresenta_usuarios(usuarios: List[Usuario]):
    """Retorna uma representação da listagem de usuários"""
    result = []
    for usuario in usuarios:
        result.append({
            "id": usuario.id,
            "nome": usuario.nome,
            "jogos": [{"id": j.id, "nome": j.nome, "plataforma": j.plataforma} for j in usuario.jogos]
        })
    return {"usuarios": result}
