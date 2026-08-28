from docx import Document as DocxDocument


def triar_docx(doc):
    try:
        docx_obj = DocxDocument(doc.caminho)
    except Exception as e:
        doc.nivel = 3
        doc.motivos.append(f"Falha ao abrir DOCX (corrompido ou protegido): {e}")
        return doc

    paragrafos = [p.text for p in docx_obj.paragraphs if p.text.strip()]

    if not paragrafos:
        doc.nivel = 3
        doc.motivos.append("Documento sem texto extraivel (pode conter so imagens/tabelas)")
        return doc

    if len(paragrafos) < 3:
        doc.nivel = 2
        doc.pipeline = "docx_texto"
        doc.motivos.append("Poucos paragrafos com texto - conteudo pode estar incompleto")
        return doc

    doc.nivel = 1
    doc.pipeline = "docx_texto"
    return doc
