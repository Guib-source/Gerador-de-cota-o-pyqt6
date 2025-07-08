import sys
from PyQt6.QtWidgets import QApplication
from ui.onibus_ui import Onibus_Ui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("styles/style.qss", "r", encoding='utf-8') as f:
        app.setStyleSheet(f.read())
    janela = Onibus_Ui()
    janela.show()
    sys.exit(app.exec())