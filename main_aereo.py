import sys
from PyQt6.QtWidgets import QApplication
from ui.aereo_ui import Aereo_Ui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Aereo_Ui()
    janela.show()
    sys.exit(app.exec())