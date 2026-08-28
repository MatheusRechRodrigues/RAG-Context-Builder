from pipelines.pipeline_vtt import processar_vtt
from pipelines.pipeline_pdf import processar_pdf
from pipelines.pipeline_docx import processar_docx
from pipelines.pipeline_xlsx import processar_xlsx
from pipelines.pipeline_pptx import processar_pptx
from pipelines.pipeline_texto import processar_texto

ROTEADOR_PIPELINES = {
    "vtt": processar_vtt,
    "pdf_texto": processar_pdf,
    "docx_texto": processar_docx,
    "xlsx_tabela": processar_xlsx,
    "pptx_texto": processar_pptx,
    "texto_puro": processar_texto,
}


def processar_documento(caminho: str, pipeline: str):
    funcao = ROTEADOR_PIPELINES.get(pipeline)
    if funcao is None:
        raise ValueError(f"Pipeline nao reconhecido: {pipeline}")
    return funcao(caminho)
