from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

class Formulario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulario")

        # Crear etiquetas y campos de texto
        self.empresalb = QLabel("Empresa:")
        self.empresaentrada = QLineEdit()
        self.empresaentrada.textChanged.connect(self.camposLlenos)

        self.correolb = QLabel("Correo:")
        self.correoentrada = QLineEdit()
        self.correoentrada.textChanged.connect(self.camposLlenos)

        self.serviciolb = QLabel("Servicio:")
        self.servicioentrada = QLineEdit()
        self.servicioentrada.textChanged.connect(self.camposLlenos)

        # Crear botones
        self.button_cancelar = QPushButton("CANCELAR")
        self.button_cancelar.setStyleSheet("background-color: #ffb9ac; color: black;")
        self.button_cancelar.setEnabled(False)
        
        self.button_guardar = QPushButton("GUARDAR")
        self.button_guardar.setStyleSheet("background-color: #ffb9ac; color: black;")
        self.button_guardar.setEnabled(False)

        # Crear layout
        layout_vertical = QVBoxLayout()
        layout_vertical.addWidget(self.empresalb)
        layout_vertical.addWidget(self.empresaentrada)
        layout_vertical.addWidget(self.correolb)
        layout_vertical.addWidget(self.correoentrada)
        layout_vertical.addWidget(self.serviciolb)
        layout_vertical.addWidget(self.servicioentrada)

        layout_horizontal = QHBoxLayout()
        layout_horizontal.addWidget(self.button_cancelar)
        layout_horizontal.addWidget(self.button_guardar)

        layout_vertical.addLayout(layout_horizontal)

        self.setLayout(layout_vertical)
        
    def camposLlenos(self):
        if self.empresaentrada.text() == "" or self.correoentrada.text() == "" or self.servicioentrada.text() == "":
            self.button_guardar.setEnabled(False)
            self.button_guardar.setStyleSheet("background-color: #ffb9ac; color: black;")
            self.button_cancelar.setEnabled(False)
            self.button_cancelar.setStyleSheet("background-color: #ffb9ac; color: black;")
        else:
            self.button_guardar.setEnabled(True)
            self.button_guardar.setStyleSheet("background-color: #FF7E67; color: black;")
            self.button_cancelar.setEnabled(True)
            self.button_cancelar.setStyleSheet("background-color: #FF7E67; color: black;")

if __name__ == "__main__":
    app = QApplication()
    form = Formulario()
    form.show()
    app.exec_()
