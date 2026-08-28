from pathlib import Path


def triar_texto(doc):
    try:
        conteudo = Path(doc.caminho).read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        doc.nivel = 3
        doc.motivos.append(f"Falha de codificacao (nao esta em UTF-8): {e}")
        return doc

    if not conteudo.strip():
        doc.nivel = 3
        doc.motivos.append("Arquivo vazio")
        return doc

    doc.nivel = 1
    doc.pipeline = "texto_puro"
    return doc
