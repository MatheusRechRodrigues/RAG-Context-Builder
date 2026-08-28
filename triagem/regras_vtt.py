import re
from pathlib import Path

RE_TIMESTAMP = re.compile(r"\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}")


def triar_vtt(doc):
    try:
        conteudo = Path(doc.caminho).read_text(encoding="utf-8")
    except Exception as e:
        doc.nivel = 3
        doc.motivos.append(f"Falha ao ler arquivo: {e}")
        return doc

    if not conteudo.strip().startswith("WEBVTT"):
        doc.nivel = 3
        doc.motivos.append("Cabecalho WEBVTT ausente ou invalido")
        return doc

    blocos = re.split(r"\n\s*\n", conteudo)
    total_cues = 0
    cues_vazios = 0
    textos_vistos = set()
    duplicados = 0

    for bloco in blocos:
        linhas = [l for l in bloco.strip().split("\n") if l.strip()]
        if not any(RE_TIMESTAMP.search(l) for l in linhas):
            continue
        total_cues += 1
        idx = next(i for i, l in enumerate(linhas) if RE_TIMESTAMP.search(l))
        texto_cue = " ".join(linhas[idx + 1:]).strip()
        if not texto_cue:
            cues_vazios += 1
        elif texto_cue in textos_vistos:
            duplicados += 1
        else:
            textos_vistos.add(texto_cue)

    if total_cues == 0:
        doc.nivel = 3
        doc.motivos.append("Nenhum cue com timestamp valido encontrado")
        return doc

    percentual_vazios = cues_vazios / total_cues

    if percentual_vazios > 0.5:
        doc.nivel = 3
        doc.motivos.append(f"{percentual_vazios:.0%} dos cues estao vazios")
        return doc

    if cues_vazios > 0 or duplicados > 0:
        doc.nivel = 2
        doc.pipeline = "vtt"
        if cues_vazios:
            doc.motivos.append(f"{cues_vazios} cue(s) vazio(s) encontrados")
        if duplicados:
            doc.motivos.append(f"{duplicados} cue(s) duplicado(s) encontrados")
        return doc

    doc.nivel = 1
    doc.pipeline = "vtt"
    return doc
