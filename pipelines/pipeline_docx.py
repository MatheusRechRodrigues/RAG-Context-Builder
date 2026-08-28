from docx import Document as DocxDocument


def processar_docx(caminho: str):
    docx_obj = DocxDocument(caminho)
    blocos = []
    for i, paragrafo in enumerate(docx_obj.paragraphs, start=1):
        texto = paragrafo.text.strip()
        if texto:
            blocos.append({"paragrafo": i, "texto": texto})
    return blocos
