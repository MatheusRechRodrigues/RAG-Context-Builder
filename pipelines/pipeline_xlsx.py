import openpyxl


def processar_xlsx(caminho: str):
    planilha = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    blocos = []
    for aba in planilha.worksheets:
        for i, linha in enumerate(aba.iter_rows(values_only=True), start=1):
            valores = [str(c) for c in linha if c is not None and str(c).strip()]
            if valores:
                blocos.append({"aba": aba.title, "linha": i, "texto": " | ".join(valores)})
    planilha.close()
    return blocos
