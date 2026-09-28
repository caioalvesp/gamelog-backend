# GameLog — API (Back-End)

API REST do **GameLog**, responsável por persistir usuários, jogos e a coleção pessoal de cada usuário (se zerou e a nota dada), além de consultar a **RAWG Video Games Database** para trazer capa, data de lançamento, desenvolvedora e nota da crítica dos jogos.

Este repositório é o módulo **API (Back-End)** do MVP (Cenário 1.1: Interface ↔ API ↔ API Externa). O módulo da interface está no repositório [gamelog-frontend](https://github.com/caioalvesp/gamelog-frontend) (onde também está a imagem de arquitetura completa).

## Stack

- Python + Flask, com [flask-openapi3](https://luolingchun.github.io/flask-openapi3/) para documentação OpenAPI (Swagger/Redoc/RapiDoc)
- SQLAlchemy + SQLite para persistência
- `requests` para consumir a API externa (RAWG)

## Rotas

| Rota | Métodos |
|---|---|
| `/jogos` | `GET`, `POST` |
| `/jogos/<id>` | `GET` |
| `/jogo` | `DELETE` |
| `/jogo/buscar-externo` | `GET` |
| `/usuarios` | `GET` |
| `/usuario` | `GET`, `POST`, `DELETE` |
| `/usuario/jogo` | `POST`, `PUT`, `DELETE` |

## API externa: RAWG Video Games Database

A rota `GET /jogo/buscar-externo?nome=<nome>` consulta `https://api.rawg.io/api/games?search=<nome>` na RAWG, trata a resposta (extrai nome, plataformas, capa, data de lançamento, desenvolvedora e nota da crítica) e devolve apenas os dados já tratados — o consumo da API externa não expõe nem redireciona para a RAWG.

É necessária uma API key gratuita, obtida em [rawg.io/apidocs](https://rawg.io/apidocs), configurada na variável de ambiente `RAWG_API_KEY`.

## Como executar

### Localmente (sem Docker)

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencha RAWG_API_KEY com sua chave gratuita da RAWG
flask run --host 0.0.0.0 --port 8000 --reload
```

Abra [http://localhost:8000/openapi](http://localhost:8000/openapi) para a documentação interativa (Swagger/Redoc/RapiDoc).

### Via Docker

```
docker build -t gamelog-backend .
docker run -p 8000:8000 --env-file .env gamelog-backend
```

(Sem um `.env`, a API sobe normalmente; apenas a rota `/jogo/buscar-externo` retorna erro até que `RAWG_API_KEY` seja configurada.)
