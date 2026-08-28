import re
from pathlib import Path

RE_TIMESTAMP = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})")


def corrigir_espacamento(texto: str) -> str:
    texto = re.sub(r"\s+-(\w)", r"-\1", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def extrair_cues(caminho: str):
    conteudo = Path(caminho).read_text(encoding="utf-8")
    blocos = re.split(r"\n\s*\n", conteudo)
    cues = []
    for bloco in blocos:
        linhas = [l for l in bloco.strip().split("\n") if l.strip()]
        if not linhas:
            continue
        idx = next((i for i, l in enumerate(linhas) if RE_TIMESTAMP.search(l)), None)
        if idx is None:
            continue
        inicio = RE_TIMESTAMP.search(linhas[idx]).group(1)
        texto = corrigir_espacamento(" ".join(linhas[idx + 1:]))
        if texto:
            cues.append({"timestamp": inicio, "texto": texto})
    return cues


def juntar_frases(cues):
    if not cues:
        return []
    agrupados = [dict(cues[0])]
    for cue in cues[1:]:
        anterior = agrupados[-1]
        if not anterior["texto"].rstrip().endswith((".", "!", "?")):
            anterior["texto"] = f"{anterior['texto']} {cue['texto']}".strip()
        else:
            agrupados.append(dict(cue))
    return agrupados


def processar_vtt(caminho: str):
    return juntar_frases(extrair_cues(caminho))
