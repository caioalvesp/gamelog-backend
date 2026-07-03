from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Produto, Comentario, Jogo
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um produtos cadastrado na base")
jogo_tag = Tag(name="Jogo", description="Adição, visualização e remoção de jogos à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """Adiciona um novo Produto à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    produto = Produto(
        nome=form.nome,
        quantidade=form.quantidade,
        valor=form.valor)
    logger.debug(f"Adicionando produto de nome: '{produto.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(produto)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado produto de nome: '{produto.nome}'")
        return apresenta_produto(produto), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos.
    """
    logger.debug(f"Coletando produtos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produtos = session.query(Produto).all()

    if not produtos:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(produtos))
        # retorna a representação de produto
        print(produtos)
        return apresenta_produtos(produtos), 200


@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """Faz a busca por um Produto a partir do id do produto

    Retorna uma representação dos produtos e comentários associados.
    """
    produto_id = query.id
    logger.debug(f"Coletando dados sobre produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{produto_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Produto econtrado: '{produto.id}'")
        # retorna a representação de produto
        return apresenta_produto(produto), 200


@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um Produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    produto_nome = unquote(unquote(query.nome))
    print(produto_nome)
    logger.debug(f"Deletando dados sobre produto #{produto_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{produto_nome}")
        return {"mesage": "Produto removido", "id": produto_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar produto #'{produto_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/cometario', tags=[comentario_tag],
          responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um produtos cadastrado na base identificado pelo id

    Retorna uma representação dos produtos e comentários associados.
    """
    produto_id  = form.produto_id
    logger.debug(f"Adicionando comentários ao produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo produto
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se produto não encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao produto '{produto_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao produto
    produto.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao produto #{produto_id}")

    # retorna a representação de produto
    return apresenta_produto(produto), 200

@app.post('/jogos', tags=[jogo_tag], responses={"200": JogoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_jogo(form: JogoSchema):
  """Adiciona um novo Jogo à base de dados

    Retorna uma representação dos jogos.   
    """

  jogo = Jogo(
    nome = form.nome,
    plataforma = form.plataforma,
    zerado = form.zerado,
    nota = form.nota
  )
  logger.debug(f"Adicionando jogo de nome: '{jogo.nome}'")
  try:
    session = Session()
    session.add(jogo)
    session.commit()
    logger.debug(f"Adicionando jogo de nome '{jogo.nome}'")
    return apresenta_jogo(jogo), 200
  
  except Exception as e:
    error_msg = "Não foi possível salvar novo item"
    logger.warning(f"Erro ao adicionar jogo '{jogo.nome}', {error_msg}")
    return {"message": error_msg}, 400

  # logger.debug(f"Coletando jogos.")
  # #criando conexão com a base
  # session = Session()
  # #fazendo a busca
  # jogos = session.query(Jogo).all()

  # if not jogos:
  #   # se não há jogos cadastrados
  #   return {"jogos": []}, 200
  # else:
  #   logger.debug(f"%d jogos encontrados" % len(jogos))
  #   # retorna a representação de jogos
  #   print(jogos)
  #   return apresenta_jogos(jogos), 200

@app.get('/jogos', tags=[jogo_tag], responses={"200": ListagemJogosSchema, "404": ErrorSchema})
def get_jogos():
  """
    Faz a busca por todos os Jogos cadastrados e retorna uma representação da listagem de jogos.
  """

  logger.debug(f"Coletando jogos...")
  session = Session()
  jogos = session.query(Jogo).all()

  if not jogos:
    return {"jogos": []}, 200
  else:
    logger.debug(f"%d jogos encontrados" % len(jogos))
    print(jogos)
    return apresenta_jogos(jogos), 200

@app.get('/jogos/<id>', tags=[jogo_tag], responses={"200": JogoViewSchema, "404": ErrorSchema})
def get_jogo(query: JogoBuscaSchema):
  """Faz a busca por um Jogo a partir do id do jogo. Retorna uma representação dos jogos.
  """

  jogo_id = query.id
  logger.debug(f"Coletando dados sobre o jogo #{jogo_id}")
  session = Session()
  jogo = session.query(Jogo).filter(Jogo.id == jogo_id).first()

  if not jogo:
    error_msg = "Jogo não encontrado na base :/"
    logger.warning(f"Erro ao buscar jogo '{jogo_nome}', {error_msg}")
    return {"message": error_msg}, 404
  else:
    logger.debug(f"Produto encontrado: '{jogo.id}'")
    return apresenta_jogo(jogo), 200

@app.delete('/jogo', tags=[jogo_tag], responses={"200": JogoDelSchema, "404": ErrorSchema})
def del_jogo(query: JogoBuscaSchema):
  """Deleta um jogo a partir do id informado. Retorna uma mensagem de confimação da remoção"""

  jogo_id = unquote(unquote(str(query.id)))
  print(jogo_id)
  logger.debug(f"Deletando dados sobre o jogo #{jogo_id}")
  session = Session()
  count = session.query(Jogo).filter(Jogo.id == jogo_id).delete()
  session.commit()

  if count:
     logger.debug(f"Deletando jogo #{jogo_id}")
     return {"message": "Jogo removido", "id": jogo_id}
  else:
     error_msg = "Jogo não encontrado na base :/"
     logger.warning(f"Erro ao deletar jogo #'{jogo_id}', {error_msg}")
     return {"message": error_msg}
