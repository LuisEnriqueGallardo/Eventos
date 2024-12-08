import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QTableWidget, QScrollArea, QTableWidgetItem, QMessageBox)
from PySide6.QtGui import QFont, QColor, QPixmap
from PySide6.QtCore import Qt
from basededatos import BaseDeDatos as bd
from GeneradorPDF import GeneradorPDF as pdf

class Recepcion(QWidget):
    def __init__(self, nombre, db):
        super().__init__()
        self.db = db
        
        self.setWindowTitle("Inicio")
        self.resize(800, 300)
        self.setStyleSheet("background-color: white;")
        self.setWindowIcon(QPixmap("UsuarioIcon.png"))
        
        # Diseño principal
        diseño_principal = QHBoxLayout()

        # Diseño del lado izquierdo
        diseño_izquierdo = QVBoxLayout()
        marco_izquierdo = QFrame()
        marco_izquierdo.setStyleSheet("background-color: #FDE0E2;")
        marco_izquierdo.setLayout(diseño_izquierdo)
        marco_izquierdo.setFixedWidth(200)
        diseño_principal.addWidget(marco_izquierdo)
        
        #Botones del lado Izquierdo
        botonEvento = QPushButton("Eventos")
        botonEvento.setStyleSheet("background-color: #FF7E67; color: white;")
        botonEvento.clicked.connect(self.ventanaEventos)
        diseño_izquierdo.addWidget(botonEvento)
        
        botonPagos = QPushButton("Pagos")
        botonPagos.setStyleSheet("background-color: #FF7E67; color: white;")
        botonPagos.clicked.connect(self.ventanaPagos)
        diseño_izquierdo.addWidget(botonPagos)

        # Diseño del lado derecho
        self.diseño_derecho = QVBoxLayout()
        marco_derecho = QFrame()
        marco_derecho.setStyleSheet("background-color: #FFFFFF;")
        marco_derecho.setLayout(self.diseño_derecho)
        diseño_principal.addWidget(marco_derecho)

        # Elementos centrales
        icono_usuario = QLabel()
        icono_usuario.setPixmap(QPixmap("UsuarioIcon.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        bienvenidaLabel = QLabel("¡Bienvenido!")
        bienvenidaLabel.setFont(QFont("Arial", 20))
        bienvenidaLabel.setContentsMargins(0, 0, 0, 0)
        
        nombreUsuario = QLabel(f"{nombre[1]} {nombre[2]}")
        nombreUsuario.setFont(QFont("Arial", 15))
        nombreUsuario.setContentsMargins(0, 0, 0, 0)
        
        self.diseño_derecho.insertWidget(0, icono_usuario, 0, Qt.AlignCenter)
        self.diseño_derecho.insertWidget(1, bienvenidaLabel, 0, Qt.AlignCenter)
        self.diseño_derecho.insertWidget(2, nombreUsuario, 0, Qt.AlignCenter)

        self.setLayout(diseño_principal)
        
    def ventanaEventos(self):
        # Limpiar el diseño lateral derecho
        for i in reversed(range(self.diseño_derecho.count())):
            widget_to_remove = self.diseño_derecho.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)
        
        # Añadir nuevo contenido para la interfaz de eventos
        buscarProovedor = QLineEdit()
        buscarProovedor.setPlaceholderText("Datos del proveedor aquí")
        
        mostrarProovedor = QTableWidget()
        mostrarProovedor.setColumnCount(4)
        mostrarProovedor.verticalHeader().setVisible(False)
        mostrarProovedor.setEditTriggers(QTableWidget.NoEditTriggers)
        mostrarProovedor.setSelectionBehavior(QTableWidget.SelectRows)
        mostrarProovedor.setHorizontalHeaderLabels(["No.", "Fecha", "Cliente", "Telefono", "Salon"])
        mostrarProovedor.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

        area_desplazamiento = QScrollArea()
        area_desplazamiento.setWidgetResizable(True)
        area_desplazamiento.setWidget(mostrarProovedor)
        self.diseño_derecho.addWidget(area_desplazamiento)
        
        # Insersión de los eventos en la tabla obtenidos de la base de datos
        eventos = self.db.consultar_eventos()
        
        if eventos:
            mostrarProovedor.setRowCount(len(eventos))
            for i, evento in enumerate(eventos):
                for j, campo in enumerate(evento):
                    item = QTableWidgetItem(str(campo))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(0, 0, 0))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    mostrarProovedor.setItem(i, j, item)
            mostrarProovedor.itemClicked.connect(self.itemClicado)
                    
        else:
            mostrarProovedor.setRowCount(1)
            mostrarProovedor.setItem(0, 0, QTableWidgetItem("No hay eventos"))
            mostrarProovedor.setColumnCount(1)
    
    def itemClicado(self, item):
        row = item.row()
        idRenglon = item.tableWidget().item(row, 0).text()
        
        # Obtener información del evento seleccionado
        evento = self.db.consultar_evento_detallado(idRenglon)
        mensaje = QMessageBox(self, windowTitle="Información del evento", text=f"""Numero: {evento[0]}\n Fecha: {evento[1]}\nCliente: {evento[2]} {evento[3]} {evento[4]}\nTeléfono: {evento[5]}\nSalón: {evento[6]},\n\nInformación adicional: {evento[7]}""")
        imprimir = mensaje.addButton("Imprimir", QMessageBox.AcceptRole)
        imprimir.clicked.connect(lambda: self.imprimir(evento))        
        mensaje.exec()
        
    def imprimir(self, evento):
        # Imprime un PDF con la información del evento seleccionado
        self.pdf = pdf(f"{evento[2]} {evento[3]} {evento[4]}.pdf")
        self.pdf.generar_evento(evento)
    
    def ventanaPagos(self):
        # Limpiar el diseño lateral derecho
        for i in reversed(range(self.diseño_derecho.count())):
            widget = self.diseño_derecho.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
                
        # Añadir nuevo contenido para la interfaz de pagos
        botonPagar = QPushButton("Pagar")
        botonPagar.setStyleSheet("background-color: #FF7E67; color: white;")
        self.diseño_derecho.addWidget(botonPagar)
        
        # Interfaz de pagos
        tablaPagos = QTableWidget()
        tablaPagos.setColumnCount(4)
        tablaPagos.setEditTriggers(QTableWidget.NoEditTriggers)
        tablaPagos.setSelectionBehavior(QTableWidget.SelectRows)
        tablaPagos.setHorizontalHeaderLabels(["No.", "Fecha", "Monto", "Estado"])
        self.diseño_derecho.addWidget(tablaPagos)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Recepcion()
    window.show()
    sys.exit(app.exec())