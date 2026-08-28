import json
import shutil
from pathlib import Path
from datetime import datetime

from config.settings import garantir_pastas, PASTA_RESULTADO_FINAL, PASTA_REVISAO_MANUAL
from triagem.triagem import classificar_documento
from pipelines import processar_documento
from processamento.manifesto import carregar_manifesto, salvar_manifesto, atualizar_manifesto
from logs.log_pendencias import registrar_pendencia


class AppController:
    def __init__(self):
        garantir_pastas()
        self.manifesto = carregar_manifesto()
        self.documentos = []

    def adicionar_arquivos(self, caminhos):
        for caminho in caminhos:
            self.documentos.append(classificar_documento(caminho))

    def adicionar_pasta(self, pasta, extensoes_ativas):
        for caminho in Path(pasta).rglob("*"):
            if caminho.is_file() and caminho.suffix.lower() in extensoes_ativas:
                self.documentos.append(classificar_documento(str(caminho)))

    def processar_tudo(self, callback_progresso=None):
        total = len(self.documentos)
        for i, doc in enumerate(self.documentos, start=1):
            self._processar_um(doc)
            if callback_progresso:
                callback_progresso(i, total, doc)
        salvar_manifesto(self.manifesto)

    def _processar_um(self, doc):
        if doc.nivel == 3:
            self._mover_para_revisao(doc)
            atualizar_manifesto(self.manifesto, doc)
            return

        try:
            blocos = processar_documento(doc.caminho, doc.pipeline)
            saida = PASTA_RESULTADO_FINAL / f"{Path(doc.caminho).stem}__{doc.hash[:8]}.json"
            with open(saida, "w", encoding="utf-8") as f:
                json.dump(blocos, f, ensure_ascii=False, indent=2)
            doc.status = "processado"
            doc.data_processamento = datetime.now().isoformat(timespec="seconds")
        except Exception as e:
            doc.nivel = 3
            doc.motivos.append(f"Falha inesperada durante processamento: {e}")
            self._mover_para_revisao(doc)

        atualizar_manifesto(self.manifesto, doc)

    def _mover_para_revisao(self, doc):
        doc.status = "revisao_manual"
        destino = PASTA_REVISAO_MANUAL / f"{doc.hash[:8]}__{Path(doc.caminho).name}"
        try:
            shutil.copy2(doc.caminho, destino)
        except Exception as e:
            doc.motivos.append(f"Falha ao copiar para revisao manual: {e}")
            destino = ""
        registrar_pendencia(doc, str(destino))
