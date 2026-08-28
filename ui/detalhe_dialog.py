import os
import subprocess
import sys
from pathlib import Path

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class DetalheDialog(QDialog):
    def __init__(self, doc, parent=None):
        super().__init__(parent)
        self.doc = doc
        self.setWindowTitle(f"Detalhes - {doc.nome}")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        layout.addWidget(self._linha(f"Arquivo: {doc.nome}"))
        layout.addWidget(self._linha(f"Tipo: {doc.tipo.upper()}"))
        layout.addWidget(self._linha(f"Tamanho: {doc.tamanho / 1024:.1f} KB"))
        layout.addWidget(self._linha(f"Nivel: {doc.nivel}"))
        layout.addWidget(self._linha(f"Status: {doc.status}"))

        if doc.motivos:
            layout.addWidget(QLabel("Problemas encontrados:"))
            for motivo in doc.motivos:
                layout.addWidget(self._linha(f"- {motivo}"))
        else:
            layout.addWidget(QLabel("Nenhum problema encontrado."))

        if doc.pipeline:
            layout.addWidget(self._linha(f"Pipeline: {doc.pipeline}"))

        botoes = QHBoxLayout()
        btn_arquivo = QPushButton("Abrir arquivo")
        btn_arquivo.clicked.connect(self._abrir_arquivo)
        btn_pasta = QPushButton("Abrir pasta")
        btn_pasta.clicked.connect(self._abrir_pasta)
        botoes.addWidget(btn_arquivo)
        botoes.addWidget(btn_pasta)
        layout.addLayout(botoes)

    def _linha(self, texto: str) -> QLabel:
        label = QLabel(texto)
        label.setWordWrap(True)
        return label

    def _abrir_arquivo(self):
        if sys.platform == "win32":
            os.startfile(self.doc.caminho)
        else:
            subprocess.run(["xdg-open", self.doc.caminho])

    def _abrir_pasta(self):
        if sys.platform == "win32":
            subprocess.run(["explorer", "/select,", self.doc.caminho])
        else:
            subprocess.run(["xdg-open", str(Path(self.doc.caminho).parent)])
