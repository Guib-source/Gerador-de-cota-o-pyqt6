import re

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QTextEdit, QPushButton, QCheckBox,
    QComboBox, QGridLayout, QVBoxLayout, QMessageBox, QDateEdit, QTimeEdit,
    QCompleter, QLabel, QGroupBox, QSpinBox
)

from PyQt6.QtCore import QDate, Qt, QLocale

from utils.utils import carregar_json, salvar_aeroporto
from modelos.aereo_model import Aereo


class Aereo_Ui(QWidget):

    def __init__(self):
        super().__init__()

        self.aeroportos_lista = carregar_json("aeroportos.json")
        self.locale = QLocale(QLocale.Language.Portuguese, QLocale.Country.Brazil)

        self.init_ui()

    def init_ui(self):

        self.setWindowTitle("✈️ Gerador de Cotações Aéreas")
        self.setMinimumSize(400, 800)

        main_layout = QVBoxLayout()
        grid = QGridLayout()

        # SEÇÕES
        self.origem_box, self.origem_widgets = self.criar_secao_voo("")
        self.destino_box, self.destino_widgets = self.criar_secao_voo("")

        self.origem = self.origem_widgets["aeroporto"]
        self.destino = self.destino_widgets["aeroporto"]

        # CHECKBOX
        self.somente_ida = QCheckBox("Somente Ida")
        self.bagagem = QCheckBox("Bagagem Despachada")

        # PASSAGEIROS
        self.passageiros = QSpinBox()
        self.passageiros.setRange(1, 10)
        self.passageiros.setValue(1)

        # VALOR
        self.valor = QLineEdit()
        self.valor.setPlaceholderText("Valor da Passagem (R$)")
        self.valor.textChanged.connect(self.formatar_valor)

        # RESULTADO
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)

        # BOTÕES
        btn_gerar = QPushButton("✈️ Gerar Cotação")
        btn_gerar.clicked.connect(self.gerar_cotacao)

        btn_copiar = QPushButton("📋 Copiar Texto")
        btn_copiar.setObjectName("btn_copiar")
        btn_copiar.clicked.connect(self.copiar_texto)

        # LAYOUT
        grid.addWidget(self.origem_box, 0, 0)
        grid.addWidget(self.destino_box, 0, 1)

        grid.addWidget(self.somente_ida, 1, 0)
        grid.addWidget(self.bagagem, 1, 1)

        grid.addWidget(self.valor, 2, 0)
        grid.addWidget(self.passageiros, 2, 1)

        grid.addWidget(btn_gerar, 3, 0, 1, 2)
        grid.addWidget(self.resultado, 4, 0, 1, 2)

        # NOVO AEROPORTO
        self.aeroporto_input = QLineEdit()
        self.aeroporto_input.setPlaceholderText("Cidade/Aeroporto")

        self.iata_input = QLineEdit()
        self.iata_input.setPlaceholderText("IATA (3 letras)")

        btn_add = QPushButton("➕ Novo Aeroporto")
        btn_add.clicked.connect(self.salvar_novo_aeroporto)

        grid.addWidget(self.aeroporto_input, 5, 0)
        grid.addWidget(self.iata_input, 5, 1)
        grid.addWidget(btn_add, 6, 0, 1, 2)

        grid.addWidget(btn_copiar, 7, 0, 1, 2)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    # -------- SEÇÃO DE VOO --------

    def criar_secao_voo(self, titulo):

        box = QGroupBox(titulo)
        layout = QGridLayout()

        aeroporto = self.criar_combo_aeroporto()
        cia = QLineEdit(placeholderText="Companhia Aérea")
        data = self.criar_data_edit()
        saida = QTimeEdit()
        chegada = QTimeEdit()
        paradas = self.criar_combo_paradas()

        saida.setDisplayFormat("HH:mm")
        chegada.setDisplayFormat("HH:mm")

        widgets = [
            ("Aeroporto:", aeroporto),
            ("Cia:", cia),
            ("Data:", data),
            ("Saída:", saida),
            ("Chegada:", chegada),
            ("Paradas:", paradas),
        ]

        for i, (texto, widget) in enumerate(widgets):
            layout.addWidget(QLabel(texto), i, 0)
            layout.addWidget(widget, i, 1)

        box.setLayout(layout)

        return box, {
            "aeroporto": aeroporto,
            "cia": cia,
            "data": data,
            "saida": saida,
            "chegada": chegada,
            "paradas": paradas
        }

    # -------- COMPONENTES --------

    def criar_combo_aeroporto(self):

        combo = QComboBox()
        combo.setEditable(True)
        combo.addItems(self.aeroportos_lista)
        combo.setCurrentIndex(-1)

        comp = combo.completer()
        comp.setFilterMode(Qt.MatchFlag.MatchContains)
        comp.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        return combo

    def criar_combo_paradas(self):

        combo = QComboBox()
        combo.addItems([
            "Vôo direto",
            "1 parada",
            "2 paradas",
            "3 ou mais paradas"
        ])

        return combo

    def criar_data_edit(self):

        data = QDateEdit()
        data.setCalendarPopup(True)
        data.setDate(QDate.currentDate())
        data.setDisplayFormat("dd/MM/yyyy")

        return data

    # -------- AÇÕES --------

    def gerar_cotacao(self):

        cotacao = Aereo(
            origem=self.origem.currentText(),
            destino=self.destino.currentText(),
            data_ida=self.origem_widgets["data"].date().toString("dd/MM/yyyy"),
            saida_ida=self.origem_widgets["saida"].text(),
            chegada_ida=self.origem_widgets["chegada"].text(),
            paradas_ida=self.origem_widgets["paradas"].currentText(),
            data_volta=self.destino_widgets["data"].date().toString("dd/MM/yyyy"),
            saida_volta=self.destino_widgets["saida"].text(),
            chegada_volta=self.destino_widgets["chegada"].text(),
            paradas_volta=self.destino_widgets["paradas"].currentText(),
            somente_ida=self.somente_ida.isChecked(),
            valor=self.valor.text(),
            cia_ida=self.origem_widgets["cia"].text(),
            cia_volta=self.destino_widgets["cia"].text(),
            quantidade_passageiros=self.passageiros.value(),
            bagagem="Inclui bagagem de mão e bagagem despachada"
            if self.bagagem.isChecked()
            else "Inclui somente bagagem de mão"
        )

        self.resultado.setPlainText(cotacao.gerar_texto())

    def copiar_texto(self):

        QApplication.clipboard().setText(self.resultado.toPlainText())
        QMessageBox.information(self, "Copiado", "Texto copiado com sucesso!")

    def salvar_novo_aeroporto(self):

        cidade = self.aeroporto_input.text().strip()
        iata = self.iata_input.text().strip().upper()

        if not cidade or len(iata) != 3:
            QMessageBox.warning(self, "Erro", "Código IATA inválido.")
            return

        if salvar_aeroporto(cidade, iata, "aeroportos.json"):

            texto = f"{cidade.title()} ({iata})"

            self.origem.addItem(texto)
            self.destino.addItem(texto)

            self.aeroporto_input.clear()
            self.iata_input.clear()

            QMessageBox.information(self, "Sucesso", f"Aeroporto {texto} adicionado!")

    def formatar_valor(self):

        numeros = re.sub(r"\D", "", self.valor.text())

        if not numeros:
            return

        valor = int(numeros) / 100
        texto = self.locale.toCurrencyString(valor)

        self.valor.blockSignals(True)
        self.valor.setText(texto)
        self.valor.blockSignals(False)