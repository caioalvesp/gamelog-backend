import os
import requests

RAWG_BASE_URL = "https://api.rawg.io/api/games"


class RawgError(Exception):
    """Erro ao consultar ou tratar a resposta da API externa RAWG."""


def _extrai_plataformas(jogo: dict) -> str:
    plataformas = jogo.get("platforms") or []
    nomes = [p["platform"]["name"] for p in plataformas if p.get("platform", {}).get("name")]
    return ", ".join(nomes)


def _extrai_desenvolvedora(jogo: dict):
    desenvolvedoras = jogo.get("developers") or []
    nomes = [d["name"] for d in desenvolvedoras if d.get("name")]
    return ", ".join(nomes) if nomes else None


def buscar_jogos(nome: str, limit: int = 8):
    """Consulta a RAWG Video Games Database por jogos que combinem com `nome`
    e retorna uma lista de dicts já tratados, prontos para a resposta da API.

    Lança RawgError se a chave não estiver configurada ou a chamada falhar.
    """
    api_key = os.environ.get("RAWG_API_KEY")
    if not api_key:
        raise RawgError("RAWG_API_KEY não configurada no ambiente")

    try:
        response = requests.get(
            RAWG_BASE_URL,
            params={"key": api_key, "search": nome, "page_size": limit},
            timeout=5,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise RawgError(f"Falha ao consultar a API externa: {e}")

    data = response.json()

    return [
        {
            "nome": jogo.get("name"),
            "plataformas": _extrai_plataformas(jogo),
            "capa_url": jogo.get("background_image"),
            "data_lancamento": jogo.get("released"),
            "desenvolvedora": _extrai_desenvolvedora(jogo),
            "nota_critica": jogo.get("metacritic"),
        }
        for jogo in data.get("results", [])
        if jogo.get("name")
    ]
