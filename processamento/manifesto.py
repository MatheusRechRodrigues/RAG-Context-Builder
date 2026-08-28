import json
from config.settings import CAMINHO_MANIFESTO


def carregar_manifesto() -> dict:
    if not CAMINHO_MANIFESTO.exists():
        return {}
    with open(CAMINHO_MANIFESTO, encoding="utf-8") as f:
        registros = json.load(f)
    return {r["hash"]: r for r in registros}


def salvar_manifesto(registros_por_hash: dict):
    with open(CAMINHO_MANIFESTO, "w", encoding="utf-8") as f:
        json.dump(list(registros_por_hash.values()), f, ensure_ascii=False, indent=2)


def ja_processado(hash_arquivo: str, manifesto: dict) -> bool:
    registro = manifesto.get(hash_arquivo)
    return registro is not None and registro.get("data_processamento") is not None


def atualizar_manifesto(manifesto: dict, doc):
    manifesto[doc.hash] = doc.to_dict()
