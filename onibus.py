import sys
from dataclasses import dataclass
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QTextEdit, QPushButton, QCheckBox, QGridLayout, QVBoxLayout, QMessageBox, QDateEdit, QTimeEdit, QLabel
)
from PyQt6.QtCore import QDate

# ----------------- DATACLASS -------------------

@dataclass
class Onibus:
    origem: str
    destino: str
    data_ida: str
    saida_ida: str
    chegada_ida: str
    data_volta: str = ""
    saida_volta: str = ""
    chegada_volta: str = ""
    somente_ida: bool = False
    valor: str = ""
    
    def gerar_texto(self) -> str:
        texto = (
            f"🚌 Segue sua cotação para a sua próxima viagem:\n\n"
            f"{self.origem} ➡️ {self.destino}\n"
            f"📅 IDA: {self.data_ida}\n"
            f"➡ Saída: {self.saida_ida}h | Chegada: {self.chegada_ida}h\n\n"
        )
        
        if not self.somente_ida:
            texto += (
                f"📅 VOLTA: {self.data_volta}\n"
                f"➡ Saída: {self.saida_volta}h | Chegada: {self.chegada_volta}h\n\n"
            )
        
        texto += (
            f"💰 Valor: R$ {self.valor}\n"
            f"Valores sujeitos à disponibilidade e alteração sem aviso prévio."
            )
        
        return texto

# ----------------- INTERFACE -------------------

class OnibusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cotação de Ônibus")
        self.setMinimumSize(400, 700)
        
        self.layout = QVBoxLayout()
        grid_layout = QGridLayout()
        
        # ----- INPUTS ORIGEM -----
        
        self.origem_input = QLineEdit(); self.origem_input.setPlaceholderText("Origem")
        
        self.data_ida_input = QDateEdit(); self.data_ida_input.setCalendarPopup(True); self.data_ida_input.setDate(QDate.currentDate())
        
        self.saida_ida_input = QTimeEdit(); self.saida_ida_input.setDisplayFormat("HH:mm")
        
        self.chegada_ida_input = QTimeEdit(); self.chegada_ida_input.setDisplayFormat("HH:mm")
        
        # ----- INPUTS DESTINO -----
        
        self.destino_input = QLineEdit(); self.destino_input.setPlaceholderText("Destino")
        
        self.data_volta_input = QDateEdit(); self.data_volta_input.setCalendarPopup(True); self.data_volta_input.setDate(QDate.currentDate())
        
        self.saida_volta_input = QTimeEdit(); self.saida_volta_input.setDisplayFormat("HH:mm")
        
        self.chegada_volta_input = QTimeEdit(); self.chegada_volta_input.setDisplayFormat("HH:mm")
        
        # ----- OUTROS INPUTS -----
        
        self.somente_ida_checkbox = QCheckBox("Somente Ida")
        
        self.valor_input = QLineEdit(); self.valor_input.setPlaceholderText("Valor (R$)")
        
        self.resultado_texto = QTextEdit(); self.resultado_texto.setReadOnly(True)
        
        # ----- BOTÕES -----
        
        self.gerar_button = QPushButton("🚌 Gerar Cotação"); self.gerar_button.clicked.connect(self.gerar_cotacao)
        
        self.copiar_button = QPushButton("📋 Copiar Texto"); self.copiar_button.clicked.connect(self.copiar_texto)
        
        # ----- Layout -----
        # ----- ORIGEM -----
        grid_layout.addWidget(QLabel("Origem:"), 0, 0)      # Label Origem
        grid_layout.addWidget(self.origem_input, 1, 0)      # Input Origem
        grid_layout.addWidget(self.data_ida_input, 2, 0)    # Data de Ida
        grid_layout.addWidget(self.saida_ida_input, 3, 0)   # Saída de Ida
        grid_layout.addWidget(self.chegada_ida_input, 4, 0) # Chegada de Ida
        
        # ----- DESTINO -----
        grid_layout.addWidget(QLabel("Destino:"), 0, 1)       # Label Destino
        grid_layout.addWidget(self.destino_input, 1, 1)       # Input Destino
        grid_layout.addWidget(self.data_volta_input, 2, 1)    # Data de Volta
        grid_layout.addWidget(self.saida_volta_input, 3, 1)   # Saída de Volta
        grid_layout.addWidget(self.chegada_volta_input, 4, 1) # Chegada de Volta
        
        # ----- OUTROS -----
        grid_layout.addWidget(self.somente_ida_checkbox, 5, 0)  # Checkbox Somente Ida
        grid_layout.addWidget(self.valor_input, 6, 0, 1, 2)     # Valor da Passagem
        grid_layout.addWidget(self.gerar_button, 7, 0, 1, 2)    # Botão Gerar Cotação
        grid_layout.addWidget(self.resultado_texto, 8, 0, 1, 2) # Resultado da Cotação
        grid_layout.addWidget(self.copiar_button, 9, 0, 1, 2)
        
        self.layout.addLayout(grid_layout)
        self.setLayout(self.layout)
        
    def gerar_cotacao(self):
        cotação = Onibus(
            origem=self.origem_input.text(),
            data_ida=self.data_ida_input.date().toString("dd/MM/yyyy"),
            saida_ida=self.saida_ida_input.text(),
            chegada_ida=self.chegada_ida_input.text(),
            destino=self.destino_input.text(),
            data_volta=self.data_volta_input.date().toString("dd/MM/yyyy"),
            saida_volta=self.saida_volta_input.text(),
            chegada_volta=self.chegada_volta_input.text(),
            somente_ida=self.somente_ida_checkbox.isChecked(),
            valor=self.valor_input.text()
            )
        
        self.resultado_texto.setPlainText(cotação.gerar_texto())
        
    def copiar_texto(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.resultado_texto.toPlainText())
        QMessageBox.information(self, "Copiado", "Texto copiado com sucesso!")
        
        
# ----------------- EXECUÇÃO -------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = OnibusWidget()
    widget.show()
    sys.exit(app.exec())
    