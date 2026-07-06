from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from model import Session, Jogo, Usuario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
jogo_tag = Tag(name="Jogo", description="Adição, visualização e remoção de jogos à base")
usuario_tag = Tag(name="Usuario", description="Adição, visualização e remoção de usuários e sua coleção de jogos")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/jogos', tags=[jogo_tag], responses={"200": JogoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_jogo(form: JogoSchema):
  """Adiciona um novo Jogo à base de dados

    Retorna uma representação dos jogos.   
    """

  jogo = Jogo(
    nome = form.nome,
    plataforma = form.plataforma
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
    logger.debug(f"Jogo encontrado: '{jogo.id}'")
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


@app.post('/usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "400": ErrorSchema})
def add_usuario(form: UsuarioSchema):
    """Adiciona um novo Usuário à base de dados.

    Retorna uma representação do usuário com sua coleção de jogos.
    """
    usuario = Usuario(nome=form.nome)
    logger.debug(f"Adicionando usuário de nome: '{usuario.nome}'")
    try:
        session = Session()
        session.add(usuario)
        session.commit()
        logger.debug(f"Adicionado usuário de nome: '{usuario.nome}'")
        return apresenta_usuario(usuario), 200

    except Exception as e:
        error_msg = "Não foi possível salvar novo usuário :/"
        logger.warning(f"Erro ao adicionar usuário '{usuario.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/usuarios', tags=[usuario_tag],
         responses={"200": ListagemUsuariosSchema, "404": ErrorSchema})
def get_usuarios():
    """Faz a busca por todos os Usuários cadastrados.

    Retorna uma representação da listagem de usuários.
    """
    logger.debug("Coletando usuários")
    session = Session()
    usuarios = session.query(Usuario).all()

    if not usuarios:
        return {"usuarios": []}, 200
    else:
        logger.debug(f"%d usuários encontrados" % len(usuarios))
        return apresenta_usuarios(usuarios), 200


@app.get('/usuario', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def get_usuario(query: UsuarioBuscaSchema):
    """Faz a busca por um Usuário a partir do seu id.

    Retorna uma representação do usuário com sua coleção de jogos.
    """
    usuario_id = query.id
    logger.debug(f"Coletando dados sobre o usuário #{usuario_id}")
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        error_msg = "Usuário não encontrado na base :/"
        logger.warning(f"Erro ao buscar usuário #{usuario_id}, {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Usuário encontrado: '{usuario.id}'")
        return apresenta_usuario(usuario), 200


@app.delete('/usuario', tags=[usuario_tag],
            responses={"200": UsuarioDelSchema, "404": ErrorSchema})
def del_usuario(query: UsuarioBuscaSchema):
    """Deleta um Usuário a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    usuario_id = query.id
    logger.debug(f"Deletando usuário #{usuario_id}")
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        error_msg = "Usuário não encontrado na base :/"
        logger.warning(f"Erro ao deletar usuário #{usuario_id}, {error_msg}")
        return {"message": error_msg}, 404

    nome = usuario.nome
    session.delete(usuario)
    session.commit()
    logger.debug(f"Deletado usuário #{usuario_id}")
    return {"message": "Usuário removido", "id": usuario_id, "nome": nome}, 200


@app.post('/usuario/jogo', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def add_jogo_usuario(form: UsuarioJogoAddSchema):
    """Associa um Jogo à coleção de um Usuário, opcionalmente informando
    se já foi zerado e a nota dada pelo usuário.

    Retorna uma representação atualizada do usuário com sua coleção de jogos.
    """
    usuario_id = form.usuario_id
    jogo_id = form.jogo_id
    logger.debug(f"Associando jogo #{jogo_id} ao usuário #{usuario_id}")
    session = Session()

    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        error_msg = "Usuário não encontrado na base :/"
        logger.warning(f"Erro ao associar jogo ao usuário #{usuario_id}, {error_msg}")
        return {"message": error_msg}, 404

    jogo = session.query(Jogo).filter(Jogo.id == jogo_id).first()
    if not jogo:
        error_msg = "Jogo não encontrado na base :/"
        logger.warning(f"Erro ao associar jogo #{jogo_id}, {error_msg}")
        return {"message": error_msg}, 404

    if jogo in usuario.jogos:
        error_msg = "Jogo já está na coleção do usuário :/"
        logger.warning(f"Jogo #{jogo_id} já associado ao usuário #{usuario_id}")
        return {"message": error_msg}, 400

    usuario.adiciona_jogo(jogo, zerado=form.zerado, nota=form.nota)
    session.commit()
    logger.debug(f"Jogo #{jogo_id} associado ao usuário #{usuario_id}")
    return apresenta_usuario(usuario), 200


@app.put('/usuario/jogo', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_jogo_usuario(form: UsuarioJogoUpdateSchema):
    """Atualiza o zerado/nota de um Jogo já presente na coleção de um Usuário.

    Retorna uma representação atualizada do usuário com sua coleção de jogos.
    """
    usuario_id = form.usuario_id
    jogo_id = form.jogo_id
    logger.debug(f"Atualizando associação jogo #{jogo_id} / usuário #{usuario_id}")
    session = Session()

    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        error_msg = "Usuário não encontrado na base :/"
        logger.warning(f"Erro ao atualizar associação, usuário #{usuario_id} não encontrado, {error_msg}")
        return {"message": error_msg}, 404

    associacao = usuario.busca_associacao(jogo_id)
    if not associacao:
        error_msg = "Jogo não encontrado na coleção do usuário :/"
        logger.warning(f"Jogo #{jogo_id} não encontrado na coleção do usuário #{usuario_id}")
        return {"message": error_msg}, 404

    if form.zerado is not None:
        associacao.zerado = form.zerado
    if form.nota is not None:
        associacao.nota = form.nota

    session.commit()
    logger.debug(f"Associação jogo #{jogo_id} / usuário #{usuario_id} atualizada")
    return apresenta_usuario(usuario), 200


@app.delete('/usuario/jogo', tags=[usuario_tag],
            responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def remove_jogo_usuario(query: UsuarioJogoSchema):
    """Remove um Jogo da coleção de um Usuário.

    Retorna uma representação atualizada do usuário com sua coleção de jogos.
    """
    usuario_id = query.usuario_id
    jogo_id = query.jogo_id
    logger.debug(f"Removendo jogo #{jogo_id} do usuário #{usuario_id}")
    session = Session()

    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        error_msg = "Usuário não encontrado na base :/"
        logger.warning(f"Erro ao remover jogo do usuário #{usuario_id}, {error_msg}")
        return {"message": error_msg}, 404

    jogo = session.query(Jogo).filter(Jogo.id == jogo_id).first()
    if not jogo or jogo not in usuario.jogos:
        error_msg = "Jogo não encontrado na coleção do usuário :/"
        logger.warning(f"Jogo #{jogo_id} não encontrado na coleção do usuário #{usuario_id}")
        return {"message": error_msg}, 404

    usuario.remove_jogo(jogo)
    session.commit()
    logger.debug(f"Jogo #{jogo_id} removido do usuário #{usuario_id}")
    return apresenta_usuario(usuario), 200
