from pydantic import BaseModel
from typing import Optional, List
from model.jogo import Jogo


class JogoSchema(BaseModel):
  """Define como um novo jogo a ser inserido deve ser representado"""
  nome: str = "Super Mario Bros."
  plataforma: str = "Super Nintendo Entertainment System"
  capa_url: Optional[str] = None
  data_lancamento: Optional[str] = None
  desenvolvedora: Optional[str] = None
  nota_critica: Optional[int] = None

class JogoBuscaSchema(BaseModel):
  """ Define como deve ser a estrutura que representa a busca, que será feita
      apenas com base no nome do jogo."""
  id: int = 1

class ListagemJogosSchema(BaseModel):
  """Define como uma listagem de jogos será retornada."""
  jogos:List[JogoSchema]

def apresenta_jogos(jogos: List[Jogo]):
  """Retorna uma representação do jogo seguindo o schema definido em JogoViewSchema"""
  return {"jogos": [apresenta_jogo(jogo) for jogo in jogos]}

class JogoViewSchema(BaseModel):
  """Define como um jogo será retornado: jogo."""
  id: int = 1
  nome: str = "Super Mario Bros."
  plataforma: str = "Super Nintendo Entertainment System"
  capa_url: Optional[str] = None
  data_lancamento: Optional[str] = None
  desenvolvedora: Optional[str] = None
  nota_critica: Optional[int] = None

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
    "capa_url": jogo.capa_url,
    "data_lancamento": jogo.data_lancamento,
    "desenvolvedora": jogo.desenvolvedora,
    "nota_critica": jogo.nota_critica
  }

class JogoBuscaExternaSchema(BaseModel):
  """Define como deve ser a estrutura da busca de um jogo na base externa (RAWG),
  feita a partir do nome do jogo."""
  nome: str = "Resident Evil"

class JogoExternoSchema(BaseModel):
  """Define como um resultado de busca na API externa (RAWG) é representado,
  já tratado pelo back-end."""
  nome: str
  plataformas: Optional[str] = None
  capa_url: Optional[str] = None
  data_lancamento: Optional[str] = None
  desenvolvedora: Optional[str] = None
  nota_critica: Optional[int] = None

class ListagemJogosExternosSchema(BaseModel):
  """Define como a listagem de resultados da busca externa será retornada."""
  resultados: List[JogoExternoSchema]