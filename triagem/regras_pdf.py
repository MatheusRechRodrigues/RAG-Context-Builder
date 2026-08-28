import pdfplumber
from config.settings import LIMIAR_CARACTERES_POR_PAGINA_PDF, LIMIAR_PERCENTUAL_PAGINAS_FRACAS


def triar_pdf(doc):
    try:
        with pdfplumber.open(doc.caminho) as pdf:
            paginas = pdf.pages
            n_paginas = len(paginas)
            if n_paginas == 0:
                doc.nivel = 3
                doc.motivos.append("PDF sem paginas")
                return doc

            paginas_fracas = 0
            total_caracteres = 0
            for pagina in paginas:
                texto = pagina.extract_text() or ""
                total_caracteres += len(texto.strip())
                if len(texto.strip()) < LIMIAR_CARACTERES_POR_PAGINA_PDF:
                    paginas_fracas += 1
    except Exception as e:
        doc.nivel = 3
        doc.pipeline = "ocr"
        doc.motivos.append(f"Falha ao abrir PDF (corrompido ou protegido): {e}")
        return doc

    percentual_fracas = paginas_fracas / n_paginas
    media_caracteres = total_caracteres / n_paginas

    if media_caracteres < LIMIAR_CARACTERES_POR_PAGINA_PDF:
        doc.nivel = 3
        doc.pipeline = "ocr"
        doc.motivos.append("PDF aparentemente escaneado")
        doc.motivos.append(
            f"Media de {media_caracteres:.1f} caracteres por pagina "
            f"({percentual_fracas:.0%} das paginas com pouco ou nenhum texto)"
        )
        return doc

    if percentual_fracas > LIMIAR_PERCENTUAL_PAGINAS_FRACAS:
        doc.nivel = 2
        doc.pipeline = "pdf_texto"
        doc.motivos.append(f"{percentual_fracas:.0%} das paginas com pouco texto extraido")
        return doc

    doc.nivel = 1
    doc.pipeline = "pdf_texto"
    return doc
