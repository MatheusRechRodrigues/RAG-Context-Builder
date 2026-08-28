from pathlib import Path


def processar_texto(caminho: str):
    conteudo = Path(caminho).read_text(encoding="utf-8").strip()
    return [{"texto": conteudo}] if conteudo else []
