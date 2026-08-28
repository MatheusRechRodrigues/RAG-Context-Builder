from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QFileDialog, QProgressBar,
    QComboBox, QLabel, QHeaderView, QListWidget, QListWidgetItem,
)
from PySide6.QtCore import Qt

from config.settings import EXTENSOES_DISPONIVEIS
from controllers.app_controller import AppController
from ui.detalhe_dialog import DetalheDialog

COLUNAS = ["Arquivo", "Tipo", "Nivel", "Status"]
FILTROS = ["Todos", "Nivel 1", "Nivel 2", "Nivel 3", "Processados", "Com alerta", "Pendentes"]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RAG Document Manager")
        self.resize(850, 550)
        self.controller = AppController()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        layout.addWidget(QLabel("Extensoes ativas para processamento:"))
        self.lista_extensoes = QListWidget()
        self.lista_extensoes.setMaximumHeight(90)
        self.lista_extensoes.setFlow(QListWidget.LeftToRight)
        for ext in EXTENSOES_DISPONIVEIS:
            item = QListWidgetItem(ext)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            self.lista_extensoes.addItem(item)
        layout.addWidget(self.lista_extensoes)

        topo = QHBoxLayout()
        btn_arquivos = QPushButton("+ Adicionar documentos")
        btn_arquivos.clicked.connect(self._adicionar_documentos)
        btn_pasta = QPushButton("+ Adicionar pasta")
        btn_pasta.clicked.connect(self._adicionar_pasta)
        topo.addWidget(btn_arquivos)
        topo.addWidget(btn_pasta)
        topo.addStretch()
        topo.addWidget(QLabel("Filtro:"))
        self.combo_filtro = QComboBox()
        self.combo_filtro.addItems(FILTROS)
        self.combo_filtro.currentTextChanged.connect(self._atualizar_tabela)
        topo.addWidget(self.combo_filtro)
        layout.addLayout(topo)

        self.tabela = QTableWidget(0, len(COLUNAS))
        self.tabela.setHorizontalHeaderLabels(COLUNAS)
        self.tabela.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.cellDoubleClicked.connect(self._abrir_detalhe)
        layout.addWidget(self.tabela)

        self.progresso = QProgressBar()
        layout.addWidget(self.progresso)

        self.label_resumo = QLabel("Nenhum documento adicionado.")
        layout.addWidget(self.label_resumo)

    def _extensoes_ativas(self):
        ativas = []
        for i in range(self.lista_extensoes.count()):
            item = self.lista_extensoes.item(i)
            if item.checkState() == Qt.Checked:
                ativas.append(item.text())
        return set(ativas)

    def _filtro_dialogo(self):
        ativas = self._extensoes_ativas()
        if not ativas:
            return "Todos os arquivos (*)"
        return "Arquivos suportados (" + " ".join(f"*{e}" for e in ativas) + ")"

    def _adicionar_documentos(self):
        caminhos, _ = QFileDialog.getOpenFileNames(self, "Selecionar documentos", "", self._filtro_dialogo())
        if caminhos:
            self.controller.adicionar_arquivos(caminhos)
            self._processar_e_atualizar()

    def _adicionar_pasta(self):
        pasta = QFileDialog.getExistingDirectory(self, "Selecionar pasta")
        if pasta:
            self.controller.adicionar_pasta(pasta, self._extensoes_ativas())
            self._processar_e_atualizar()

    def _processar_e_atualizar(self):
        def callback(i, total, doc):
            self.progresso.setValue(int(i / total * 100))
            self._atualizar_tabela()
            self.repaint()

        self.controller.processar_tudo(callback_progresso=callback)
        self._atualizar_tabela()
        self._atualizar_resumo()

    def _atualizar_resumo(self):
        docs = self.controller.documentos
        n1 = sum(1 for d in docs if d.nivel == 1)
        n2 = sum(1 for d in docs if d.nivel == 2)
        n3 = sum(1 for d in docs if d.nivel == 3)
        self.label_resumo.setText(
            f"Total: {len(docs)} | Nivel 1: {n1} | Nivel 2: {n2} | Nivel 3 (revisao manual): {n3}"
        )

    def _atualizar_tabela(self):
        filtro = self.combo_filtro.currentText()
        documentos = self._filtrar(self.controller.documentos, filtro)
        self.tabela.setRowCount(len(documentos))
        for linha, doc in enumerate(documentos):
            self.tabela.setItem(linha, 0, QTableWidgetItem(doc.nome))
            self.tabela.setItem(linha, 1, QTableWidgetItem(doc.tipo.upper()))
            self.tabela.setItem(linha, 2, QTableWidgetItem(str(doc.nivel)))
            self.tabela.setItem(linha, 3, QTableWidgetItem(doc.status))

    def _filtrar(self, documentos, filtro):
        if filtro == "Todos":
            return documentos
        if filtro == "Nivel 1":
            return [d for d in documentos if d.nivel == 1]
        if filtro == "Nivel 2":
            return [d for d in documentos if d.nivel == 2]
        if filtro == "Nivel 3":
            return [d for d in documentos if d.nivel == 3]
        if filtro == "Processados":
            return [d for d in documentos if d.status == "processado"]
        if filtro == "Com alerta":
            return [d for d in documentos if d.nivel == 2]
        if filtro == "Pendentes":
            return [d for d in documentos if d.status == "revisao_manual"]
        return documentos

    def _abrir_detalhe(self, linha, _coluna):
        filtro = self.combo_filtro.currentText()
        documentos = self._filtrar(self.controller.documentos, filtro)
        doc = documentos[linha]
        DetalheDialog(doc, parent=self).exec()
