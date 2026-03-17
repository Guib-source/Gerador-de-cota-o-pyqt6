import sys, os
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
        self.setMinimumSize(400, 800)

        # Layout principal
        main_layout = QHBoxLayout()
        container = QWidget(); container.setObjectName('main_container')
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Sidebar
        sidebar = QVBoxLayout(); sidebar.setObjectName('sidebar')
        sidebar.setAlignment(Qt.AlignmentFlag.AlignTop)

        btn_aereo = QPushButton("✈️"); btn_aereo.setObjectName('btn_sidebar')
        btn_onibus = QPushButton("🚌"); btn_onibus.setObjectName('btn_sidebar')
        sidebar.addWidget(btn_aereo)
        sidebar.addWidget(btn_onibus)
        
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar")
        sidebar.setAlignment(Qt.AlignmentFlag.AlignTop)
        sidebar_widget.setLayout(sidebar)

        # Conteúdo principal com QStackedWidget
        self.stack = QStackedWidget()
        self.aereo_ui = Aereo_Ui()
        self.onibus_ui = Onibus_Ui()
        self.stack.addWidget(self.aereo_ui)
        self.stack.addWidget(self.onibus_ui)

        # Adiciona sidebar e stack no layout principal
        main_layout.addWidget(sidebar_widget, 1)
        main_layout.addWidget(self.stack, 5)

        # Conecta botões
        btn_aereo.clicked.connect(lambda: self.stack.setCurrentWidget(self.aereo_ui))
        btn_onibus.clicked.connect(lambda: self.stack.setCurrentWidget(self.onibus_ui))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_path = os.path.join(os.path.dirname(__file__), "styles", "style.qss")
    with open(style_path, "r", encoding='utf-8') as f:
        app.setStyleSheet(f.read())

    janela = MainWindow()
    janela.show()

    sys.exit(app.exec())
