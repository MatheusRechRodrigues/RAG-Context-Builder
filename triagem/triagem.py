from pathlib import Path
from datetime import datetime

from models.documento import Documento
from processamento.hash_utils import calcular_hash
from triagem.regras_vtt import triar_vtt
from triagem.regras_pdf import triar_pdf
from triagem.regras_docx import triar_docx
from triagem.regras_xlsx import triar_xlsx
from triagem.regras_pptx import triar_pptx
from triagem.regras_texto import triar_texto

ROTEADOR = {
    ".vtt": triar_vtt,
    ".pdf": triar_pdf,
    ".docx": triar_docx,
    ".xlsx": triar_xlsx,
    ".pptx": triar_pptx,
    ".txt": triar_texto,
    ".md": triar_texto,
}


def classificar_documento(caminho: str) -> Documento:
    path = Path(caminho)
    extensao = path.suffix.lower()

    doc = Documento(
        caminho=str(path.resolve()),
        nome=path.name,
        tipo=extensao.lstrip("."),
        tamanho=path.stat().st_size,
        hash=calcular_hash(str(path)),
    )
    doc.data_triagem = datetime.now().isoformat(timespec="seconds")

    if extensao not in ROTEADOR:
        doc.nivel = 3
        doc.motivos.append(f"Formato nao suportado: {extensao or '(sem extensao)'}")
        return doc

    if doc.tamanho == 0:
        doc.nivel = 3
        doc.motivos.append("Arquivo vazio (0 bytes)")
        return doc

    doc = ROTEADOR[extensao](doc)
    doc.status = "revisao_manual" if doc.nivel == 3 else "automatico"
    return doc
