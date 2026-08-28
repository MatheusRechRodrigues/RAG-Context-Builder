import csv
from datetime import datetime
from config.settings import CAMINHO_LOG_PENDENCIAS

CAMPOS = [
    "arquivo", "caminho_original", "caminho_copia", "tipo", "nivel",
    "motivo", "pipeline_recomendado", "data", "status",
]


def registrar_pendencia(doc, caminho_copia: str = ""):
    novo = not CAMINHO_LOG_PENDENCIAS.exists()
    with open(CAMINHO_LOG_PENDENCIAS, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
        if novo:
            writer.writeheader()
        writer.writerow({
            "arquivo": doc.nome,
            "caminho_original": doc.caminho,
            "caminho_copia": caminho_copia,
            "tipo": doc.tipo,
            "nivel": doc.nivel,
            "motivo": " | ".join(doc.motivos),
            "pipeline_recomendado": doc.pipeline or "revisao_manual",
            "data": datetime.now().isoformat(timespec="seconds"),
            "status": "pendente",
        })
