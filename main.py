import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QStackedWidget, QHBoxLayout
)
from PyQt6.QtCore import Qt

from ui.aereo_ui import Aereo_Ui
from ui.onibus_ui import Onibus_Ui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Cotações")
        self.setMinimumSize(400, 775)

        # Layout principal
        main_layout = QHBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Sidebar
        sidebar = QVBoxLayout()
        sidebar.setAlignment(Qt.AlignmentFlag.AlignTop)

        btn_aereo = QPushButton("Aérea")
        btn_onibus = QPushButton("Ônibus")
        sidebar.addWidget(btn_aereo)
        sidebar.addWidget(btn_onibus)

        # Conteúdo principal com QStackedWidget
        self.stack = QStackedWidget()
        self.aereo_ui = Aereo_Ui()
        self.onibus_ui = Onibus_Ui()
        self.stack.addWidget(self.aereo_ui)
        self.stack.addWidget(self.onibus_ui)

        # Adiciona sidebar e stack no layout principal
        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.stack, 5)

        # Conecta botões
        btn_aereo.clicked.connect(lambda: self.stack.setCurrentWidget(self.aereo_ui))
        btn_onibus.clicked.connect(lambda: self.stack.setCurrentWidget(self.onibus_ui))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("styles/style.qss", "r", encoding='utf-8') as f:
        app.setStyleSheet(f.read())

    janela = MainWindow()
    janela.show()

    sys.exit(app.exec())
