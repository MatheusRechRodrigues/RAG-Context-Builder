from pathlib import Path

PASTA_BASE = Path.cwd()
PASTA_RESULTADO_FINAL = PASTA_BASE / "resultado_final"
PASTA_REVISAO_MANUAL = PASTA_BASE / "revisao_manual"

CAMINHO_MANIFESTO = PASTA_RESULTADO_FINAL / "manifesto_triagem.json"
CAMINHO_LOG_PENDENCIAS = PASTA_REVISAO_MANUAL / "log_pendencias.csv"

LIMIAR_CARACTERES_POR_PAGINA_PDF = 50
LIMIAR_PERCENTUAL_PAGINAS_FRACAS = 0.3

EXTENSOES_DISPONIVEIS = [".vtt", ".pdf", ".docx", ".xlsx", ".pptx", ".txt", ".md"]


def garantir_pastas():
    PASTA_RESULTADO_FINAL.mkdir(exist_ok=True)
    PASTA_REVISAO_MANUAL.mkdir(exist_ok=True)
