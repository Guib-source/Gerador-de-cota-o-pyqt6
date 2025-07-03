import sys
import json
import os
from dataclasses import dataclass
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QTextEdit, QPushButton, QCheckBox,
    QComboBox, QGridLayout, QVBoxLayout, QMessageBox, QDateEdit, QTimeEdit, QCompleter, QLabel
)
from PyQt6.QtCore import QDate, Qt


# ----------------- FUNÇÕES ADICIONAIS -------------------
def caminho_json():
    return os.path.join(os.path.dirname(__file__), "aeroportos.json")

def carregar_aeroportos():
    with open(caminho_json(), encoding="utf-8") as f:
        dados = json.load(f)
    return [f"{item['Cidade']} ({item['IATA']})" for item in dados]

def salvar_aeroporto(cidade: str, iata: str):
    caminho = caminho_json()
    with open(caminho, encoding='utf-8') as f:
        dados = json.load(f)
    
    if any(item['IATA'].upper() == iata.upper() for item in dados):
        QMessageBox.warning(None, 'Duplicado', f'O aeroporto com IATA {iata.upper()} já existe.')
        return False
    
    novo = {'Cidade': cidade.title(), 'IATA': iata.upper()}
    dados.append(novo)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f , indent=2, ensure_ascii=False)
    return True
        
# ----------------- DATACLASS -------------------

@dataclass
class Cotacao:
    origem: str
    destino: str
    data_ida: str
    saida_ida: str
    chegada_ida: str
    paradas_ida: str
    data_volta: str = ""
    saida_volta: str = ""
    chegada_volta: str = ""
    paradas_volta: str = ""
    somente_ida: bool = False
    valor: str = ""
    bagagem: str = "Não incluída"

    def gerar_texto(self) -> str:
        texto = (
            f"✈️ Segue sua cotação especial para a sua próxima viagem:\n\n"
            f"{self.origem} ➡️ {self.destino}\n"
            f"📅 IDA: {self.data_ida}\n"
            f"➡ Saída: {self.saida_ida}h | {self.paradas_ida}\n"
            f"➡ Chegada: {self.chegada_ida}h em {self.destino}\n\n"
        )

        if not self.somente_ida:
            texto += (
                f"{self.destino} ➡️ {self.origem}\n"
                f"📅 VOLTA: {self.data_volta}\n"
                f"➡ Saída: {self.saida_volta}h | {self.paradas_volta}\n"
                f"➡ Chegada: {self.chegada_volta}h em {self.origem}\n\n"
                f"💰 Valor: R$ {self.valor} (ida e volta)\n"
                f"🧳 Bagagem: {self.bagagem}\n\n"
                f"Valores sujeitos à disponibilidade e alteração sem aviso prévio."
            )
        else:
            texto += (
                f"💰 Valor: R$ {self.valor} (somente ida)\n"
                f"🧳 Bagagem: {self.bagagem}\n\n"
                f"Valores sujeitos à disponibilidade e alteração sem aviso prévio."
            )

        return texto

# ----------------- INTERFACE -------------------

class CotacaoAereaApp(QWidget):
    def __init__(self):
        aeroportos = carregar_aeroportos()
        
        super().__init__()
        self.setWindowTitle("✈️ Gerador de Cotações Aéreas")
        self.setMinimumSize(400, 700)

        self.layout = QVBoxLayout()
        self.grid = QGridLayout()
        
        self.aeroporto_ida_label = QLabel('Origem')
        self.aeroporto_volta_label = QLabel('Destino')

        # Entradas
        self.origem = QComboBox(); self.origem.addItems(aeroportos); self.origem.setCurrentIndex(-1); self.origem.setEditable(True); self.origem.completer().setCompletionMode(QCompleter.CompletionMode.PopupCompletion); self.origem.completer().setFilterMode(Qt.MatchFlag.MatchContains)
        self.destino = QComboBox(); self.destino.addItems(aeroportos); self.destino.setCurrentIndex(-1); self.destino.setEditable(True); self.destino.completer().setCompletionMode(QCompleter.CompletionMode.PopupCompletion); self.destino.completer().setFilterMode(Qt.MatchFlag.MatchContains)

        self.data_ida = QDateEdit(); self.data_ida.setCalendarPopup(True); self.data_ida.setDate(QDate.currentDate())
        self.data_volta = QDateEdit(); self.data_volta.setCalendarPopup(True); self.data_volta.setDate(QDate.currentDate())

        self.hora_ida = QTimeEdit()
        self.chegada_ida = QTimeEdit()

        self.hora_volta = QTimeEdit()
        self.chegada_volta = QTimeEdit()

        self.paradas_ida = QComboBox(); self.paradas_ida.addItems(["Direto", "1 Parada", "2 Paradas"])
        self.paradas_volta = QComboBox(); self.paradas_volta.addItems(["Direto", "1 Parada", "2 Paradas"])

        self.somente_ida = QCheckBox("Somente Ida")
        self.bagagem = QCheckBox("Bagagem Despachada")

        self.valor = QLineEdit(); self.valor.setPlaceholderText("Valor da Passagem (R$)")

        self.resultado = QTextEdit(); self.resultado.setReadOnly(True)
        
        self.aeroporto = QLineEdit(); self.aeroporto.setPlaceholderText("Aeroporto")
        self.IATA = QLineEdit(); self.IATA.setPlaceholderText("IATA")

        # Botões
        btn_gerar = QPushButton("✈️ Gerar Cotação"); btn_gerar.clicked.connect(self.gerar_cotacao)
        btn_copiar = QPushButton("📋 Copiar Texto"); btn_copiar.clicked.connect(self.copiar_texto)
        btn_adicionar = QPushButton("➕ Adicionar Aeroporto"); btn_adicionar.clicked.connect(self.salvar_novo_aeroporto)

        # Layout
        self.grid.addWidget(self.aeroporto_ida_label, 0, 0)
        self.grid.addWidget(self.aeroporto_volta_label, 0, 1)
        
        self.grid.addWidget(self.origem, 1, 0)
        self.grid.addWidget(self.destino, 1, 1)

        self.grid.addWidget(self.data_ida, 2, 0)
        self.grid.addWidget(self.data_volta, 2, 1)

        self.grid.addWidget(self.hora_ida, 3, 0)
        self.grid.addWidget(self.hora_volta, 3, 1)

        self.grid.addWidget(self.chegada_ida, 4, 0)
        self.grid.addWidget(self.chegada_volta, 4, 1)

        self.grid.addWidget(self.paradas_ida, 5, 0)
        self.grid.addWidget(self.paradas_volta, 5, 1)

        self.grid.addWidget(self.somente_ida, 6, 0)
        self.grid.addWidget(self.bagagem, 6, 1)

        self.grid.addWidget(self.valor, 7, 0, 1, 2)
        self.grid.addWidget(btn_gerar, 8, 0, 1, 2)
        self.grid.addWidget(self.resultado, 9, 0, 1, 2)
        self.grid.addWidget(btn_copiar, 10, 0, 1, 2)
        
        self.grid.addWidget(self.aeroporto, 11, 0, 1, 2)
        self.grid.addWidget(self.IATA, 12, 0, 1, 2)
        self.grid.addWidget(btn_adicionar, 13, 0, 1, 2)

        self.layout.addLayout(self.grid)
        self.setLayout(self.layout)

    def gerar_cotacao(self):
        cotacao = Cotacao(
            origem=self.origem.currentText(),
            destino=self.destino.currentText(),
            data_ida=self.data_ida.date().toString("dd/MM/yyyy"),
            saida_ida=self.hora_ida.text(),
            chegada_ida=self.chegada_ida.text(),
            paradas_ida=self.paradas_ida.currentText(),
            data_volta=self.data_volta.date().toString("dd/MM/yyyy"),
            saida_volta=self.hora_volta.text(),
            chegada_volta=self.chegada_volta.text(),
            paradas_volta=self.paradas_volta.currentText(),
            somente_ida=self.somente_ida.isChecked(),
            valor=self.valor.text(),
            bagagem="Inclui bagagem de mão e bagagem despachada" if self.bagagem.isChecked() else "Inclui somente bagagem de mão (sem bagagem despachada)"
        )

        self.resultado.setPlainText(cotacao.gerar_texto())


    def copiar_texto(self):
        texto = self.resultado.toPlainText()
        QApplication.clipboard().setText(texto)
        QMessageBox.information(self, "Copiado", "Texto copiado com sucesso!")

    def salvar_novo_aeroporto(self):
        cidade = self.aeroporto.text().strip()
        iata = self.IATA.text().strip()
        
        if not cidade or not iata or len(iata) !=3:
            QMessageBox.warning(self, 'ERRO', 'Preencha a cidade e um código IATA válido (03 letras).')
            return
        
        if salvar_aeroporto(cidade, iata):
            QMessageBox.information(self, "Sucesso", f"Aeroporto '{cidade.title()} ({iata})' adicionado!")
            novo_texto = f"{cidade.title()} ({iata})"
            self.origem.addItem(novo_texto)
            self.destino.addItem(novo_texto)
            self.aeroporto.clear()
            self.IATA.clear()
        

# ----------------- EXECUÇÃO -------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = CotacaoAereaApp()
    janela.show()
    sys.exit(app.exec())
