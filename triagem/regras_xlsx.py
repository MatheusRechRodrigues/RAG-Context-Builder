import openpyxl


def triar_xlsx(doc):
    try:
        planilha = openpyxl.load_workbook(doc.caminho, read_only=True, data_only=True)
    except Exception as e:
        doc.nivel = 3
        doc.motivos.append(f"Falha ao abrir XLSX (corrompido ou protegido): {e}")
        return doc

    total_linhas = 0
    for aba in planilha.worksheets:
        for linha in aba.iter_rows(values_only=True):
            if any(c is not None and str(c).strip() for c in linha):
                total_linhas += 1
    planilha.close()

    if total_linhas == 0:
        doc.nivel = 3
        doc.motivos.append("Planilha sem dados encontrados em nenhuma aba")
        return doc

    if total_linhas < 3:
        doc.nivel = 2
        doc.pipeline = "xlsx_tabela"
        doc.motivos.append("Poucas linhas com dado - planilha pode estar incompleta")
        return doc

    doc.nivel = 1
    doc.pipeline = "xlsx_tabela"
    return doc
