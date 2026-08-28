import pdfplumber


def processar_pdf(caminho: str):
    blocos = []
    with pdfplumber.open(caminho) as pdf:
        for i, pagina in enumerate(pdf.pages, start=1):
            texto = (pagina.extract_text() or "").strip()
            if texto:
                blocos.append({"pagina": i, "texto": texto})
    return blocos
