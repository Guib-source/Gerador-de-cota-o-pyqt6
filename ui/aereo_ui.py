from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QTextEdit, QPushButton, QCheckBox,
    QComboBox, QGridLayout, QVBoxLayout, QMessageBox, QDateEdit, QTimeEdit, QCompleter, QLabel
)
from PyQt6.QtCore import QDate, Qt

class Aereo_Ui(QWidget):
    def __init__(self):
        from utils.utils import carregar_json
        aeroportos = carregar_json('aeroportos.json')
        
        super().__init__()
        self.setWindowTitle("✈️ Gerador de Cotações Aéreas")
        self.setMinimumSize(400, 775)

        self.layout = QVBoxLayout()
        grid_layout = QGridLayout()
        
        # --------- INPUTS ORIGEM ----------
        
        self.origem = QComboBox(); self.origem.addItems(aeroportos); self.origem.setCurrentIndex(-1); self.origem.setEditable(True); self.origem.completer().setCompletionMode(QCompleter.CompletionMode.PopupCompletion); self.origem.completer().setFilterMode(Qt.MatchFlag.MatchContains)
        
        self.data_ida = QDateEdit(); self.data_ida.setCalendarPopup(True); self.data_ida.setDate(QDate.currentDate())
    
        self.hora_ida = QTimeEdit(); self.hora_ida.setDisplayFormat("HH:mm")
        
        self.chegada_ida = QTimeEdit(); self.chegada_ida.setDisplayFormat("HH:mm")
        
        self.paradas_ida = QComboBox(); self.paradas_ida.addItems(["Direto", "1 Parada", "2 Paradas"])
        
        # --------- INPUTS DESTINO ----------
        
        self.destino = QComboBox(); self.destino.addItems(aeroportos); self.destino.setCurrentIndex(-1); self.destino.setEditable(True); self.destino.completer().setCompletionMode(QCompleter.CompletionMode.PopupCompletion); self.destino.completer().setFilterMode(Qt.MatchFlag.MatchContains)
        
        self.data_volta = QDateEdit(); self.data_volta.setCalendarPopup(True); self.data_volta.setDate(QDate.currentDate())

        self.hora_volta = QTimeEdit(); self.hora_volta.setDisplayFormat("HH:mm")
        
        self.chegada_volta = QTimeEdit(); self.chegada_volta.setDisplayFormat("HH:mm")

        self.paradas_volta = QComboBox(); self.paradas_volta.addItems(["Direto", "1 Parada", "2 Paradas"])
        
        # --------- OUTROS INPUTS ----------
        
        self.somente_ida = QCheckBox("Somente Ida")
        
        self.bagagem = QCheckBox("Bagagem Despachada")

        self.valor = QLineEdit(); self.valor.setPlaceholderText("Valor da Passagem (R$)")

        self.resultado = QTextEdit(); self.resultado.setReadOnly(True)
        
        self.aeroporto = QLineEdit(); self.aeroporto.setPlaceholderText("Aeroporto")
        
        self.IATA = QLineEdit(); self.IATA.setPlaceholderText("IATA")

        # -------- BOTÕES ----------
        self.btn_gerar = QPushButton("✈️ Gerar Cotação"); self.btn_gerar.clicked.connect(self.gerar_cotacao)
        
        self.btn_copiar = QPushButton("📋 Copiar Texto"); self.btn_copiar.clicked.connect(self.copiar_texto); self.btn_copiar.setObjectName('btn_copiar')
        
        self.btn_adicionar = QPushButton("➕ Adicionar Aeroporto"); self.btn_adicionar.clicked.connect(self.salvar_novo_aeroporto)
        
        # --------- ORGANIZAÇÃO DO LAYOUT ----------
        # ---------         ORIGEM        ---------- 
        grid_layout.addWidget(QLabel('Origem'), 0, 0) # Label Origem
        grid_layout.addWidget(self.origem, 1, 0)      # ComboBox Origem   
        grid_layout.addWidget(self.data_ida, 2, 0)    # Data de Ida
        grid_layout.addWidget(self.hora_ida, 3, 0)    # Hora de Ida
        grid_layout.addWidget(self.chegada_ida, 4, 0) # Chegada de Ida
        grid_layout.addWidget(self.paradas_ida, 5, 0) # Paradas de Ida
        
        # ---------         DESTINO       ----------
        grid_layout.addWidget(QLabel('Destino'), 0, 1)  # Label Destino
        grid_layout.addWidget(self.destino, 1, 1)       # ComboBox Destino
        grid_layout.addWidget(self.data_volta, 2, 1)    # Data de Volta
        grid_layout.addWidget(self.hora_volta, 3, 1)    # Hora de Volta
        grid_layout.addWidget(self.chegada_volta, 4, 1) # Chegada de Volta
        grid_layout.addWidget(self.paradas_volta, 5, 1) # Paradas de Volta

        # ---------         OUTROS        ----------
        grid_layout.addWidget(self.somente_ida, 6, 0)     # Checkbox Somente Ida
        grid_layout.addWidget(self.bagagem, 6, 1)         # Checkbox Bagagem Despachada
        grid_layout.addWidget(self.valor, 7, 0, 1, 2)     # Valor da Passagem
        grid_layout.addWidget(self.btn_gerar, 8, 0, 1, 2)      # Botão Gerar Cotação
        grid_layout.addWidget(self.resultado, 9, 0, 1, 2) # Resultado da Cotação
        grid_layout.addWidget(self.btn_copiar, 10, 0, 1, 2)    # Botão Copiar Texto
        
        # ---------         ADICIONAR AEROPORTO        ----------
        grid_layout.addWidget(self.aeroporto, 11, 0, 1, 2) # Campo para adicionar novo aeroporto
        grid_layout.addWidget(self.IATA, 12, 0, 1, 2)      # Campo para adicionar novo IATA
        grid_layout.addWidget(self.btn_adicionar, 13, 0, 1, 2)  # Botão para adicionar novo aeroporto

        self.layout.addLayout(grid_layout)
        self.setLayout(self.layout)

    def gerar_cotacao(self):
        from modelos.aereo_model import Aereo
        cotacao = Aereo(
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
        from utils.utils import salvar_aeroporto
        cidade = self.aeroporto.text().strip()
        iata = self.IATA.text().strip()
        
        if not cidade or not iata or len(iata) !=3:
            QMessageBox.warning(self, 'ERRO', 'Preencha a cidade e um código IATA válido (03 letras).')
            return
        
        if salvar_aeroporto(cidade, iata, 'aeroportos.json'):
            QMessageBox.information(self, "Sucesso", f"Aeroporto '{cidade.title()} ({iata.upper()})' adicionado!")
            novo_texto = f"{cidade.title()} ({iata.upper()})"
            self.origem.addItem(novo_texto)
            self.destino.addItem(novo_texto)
            self.aeroporto.clear()
            self.IATA.clear()