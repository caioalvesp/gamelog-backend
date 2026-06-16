from pydantic import BaseModel
from typing import Optional, List
from model.produto import Produto
from model.jogo import Jogo

class JogoSchema(BaseModel):
  """Define como um novo jogo a ser inserido deve ser representado"""
  nome: str = "Super Mario Bros."
  plataforma: str = "Super Nintendo Entertainment System"
  zerado: bool = False
  nota: int = 9

class JogoBuscaSchema(BaseModel):
  """ Define como deve ser a estrutura que representa a busca, que será feita
      apenas com base no nome do jogo."""
  id: int = 1

class ListagemJogosSchema(BaseModel):
  """Define como uma listagem de jogos será retornada."""
  jogos:List[JogoSchema]

def apresenta_jogos(jogos: List[Jogo]):
  """Retorna uma representação do produto seguindo o schema definido em JogoViewSchema"""
  result = []
  for jogo in jogos:
    result.append({
      "nome": jogo.nome,
      "plataforma": jogo.plataforma,
      "zerado": jogo.zerado,
      "nota": jogo.nota
    })

  return {"jogos": result}

class JogoViewSchema(BaseModel):
  """Define como um jogo será retornado: jogo."""
  id: int = 1
  nome: str = "Super Mario Bros."
  plataforma: str = "Super Nintendo Entertainment System"
  zerado: bool = False
  nota: int = 8

class JogoDelSchema(BaseModel):
  """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção. """

  message:str
  id:int
  nome:str

def apresenta_jogo(jogo: Jogo):
  """ Retorna uma representação do jogo seguindo o schema definido em JogoViewSchema. """
  return {
    "id": jogo.id,
    "nome": jogo.nome,
    "plataforma": jogo.plataforma,
    "zerado": jogo.zerado,
    "nota": jogo.nota
  }