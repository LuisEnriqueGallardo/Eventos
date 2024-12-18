import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QTableWidget, QScrollArea, QTableWidgetItem, QMessageBox, QHeaderView)
from PySide6.QtGui import QFont, QColor, QPixmap
from PySide6.QtCore import Qt
from basededatos import BaseDeDatos as bd
from GeneradorPDF import GeneradorPDF as pdf

class Recepcion(QWidget):
    def __init__(self, nombre, db):
        super().__init__()
        self.db = db
        
        self.setWindowTitle("Inicio")
        self.resize(900, 400)
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

        botonEventosPagados = QPushButton("Eventos Pagados")
        botonEventosPagados.setStyleSheet("background-color: #FF7E67; color: white;")
        botonEventosPagados.clicked.connect(self.ventana_eventos_pagados)
        diseño_izquierdo.addWidget(botonEventosPagados)

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
        self.limpiar()
        
        # Añadir nuevo contenido para la interfaz de eventos
        buscarProovedor = QLineEdit()
        buscarProovedor.setPlaceholderText("Datos del proveedor aquí")
        
        mostrarProovedor = QTableWidget()
        mostrarProovedor.setColumnCount(7)
        mostrarProovedor.verticalHeader().setVisible(False)
        mostrarProovedor.setEditTriggers(QTableWidget.NoEditTriggers)
        mostrarProovedor.setSelectionBehavior(QTableWidget.SelectRows)
        mostrarProovedor.setHorizontalHeaderLabels(["No.", "Fecha", "Descripción", "Nombres", "Total", "Anticipo", "Servicio"])
        mostrarProovedor.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        mostrarProovedor.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        area_desplazamiento = QScrollArea()
        area_desplazamiento.setWidgetResizable(True)
        area_desplazamiento.setWidget(mostrarProovedor)
        self.diseño_derecho.addWidget(area_desplazamiento)
        
        # Insersión de los eventos en la tabla obtenidos de la base de datos
        eventos = self.db.consultar_eventos_no_pagados()
        
        if eventos:
            mostrarProovedor.setRowCount(len(eventos))
            for i, evento in enumerate(eventos):
                for j, campo in enumerate(evento):
                    if campo == None:
                        campo = "N/A"
                    item = QTableWidgetItem(str(campo))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(0, 0, 0))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    mostrarProovedor.setItem(i, j, item)
            mostrarProovedor.itemClicked.connect(self.eventoClicado)
                    
        else:
            mostrarProovedor.setRowCount(1)
            mostrarProovedor.setItem(0, 0, QTableWidgetItem("No hay eventos"))
            mostrarProovedor.setColumnCount(1)
    
    def eventoClicado(self, item):
        row = item.row()
        idRenglon = item.tableWidget().item(row, 0).text()
        
        # Obtener información del evento seleccionado
        evento = self.db.consultar_evento_detallado(idRenglon)
        mensaje = QMessageBox(self)
        mensaje.setWindowTitle("Información del evento")
        mensaje.setText(f"""Numero: {evento[0]}\n Fecha: {evento[1]}\nCliente: {evento[2]} {evento[3]} {evento[4]}\nTeléfono: {evento[5]}\nSalón: {evento[6]},\n\nInformación adicional: {evento[7]}""")
        cerrar = mensaje.addButton("Cerrar", QMessageBox.RejectRole)
        imprimirbt = mensaje.addButton("Imprimir", QMessageBox.AcceptRole)
        imprimirbt.clicked.connect(lambda: self.imprimirNoPagado(evento))
        
        mensaje.exec_()
    
    def imprimirNoPagado(self, evento):
        # Imprime un PDF con la información del evento seleccionado
        self.pdf = pdf()
        self.pdf.generar_evento(evento)
    
    def ventanaPagos(self):
        # Limpiar el diseño lateral derecho
        self.limpiar()
                
        # Interfaz de pagos
        tablaPagos = QTableWidget()
        tablaPagos.setColumnCount(7)
        tablaPagos.setEditTriggers(QTableWidget.NoEditTriggers)
        tablaPagos.setSelectionBehavior(QTableWidget.SelectRows)
        tablaPagos.verticalHeader().setVisible(False)
        tablaPagos.setHorizontalHeaderLabels(["No.", "No. Evento", "P.I", "Fecha", "Fecha", "Estado", "Cliente"])
        tablaPagos.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.diseño_derecho.addWidget(tablaPagos)

        # Insersión de los pagos en la tabla obtenidos de la base de datos
        pagos = self.db.consultar_Pagos()
        if pagos:
            tablaPagos.setRowCount(len(pagos))
            for i, pago in enumerate(pagos):
                nombreCliente = self.db.consultar_Cliente_porEvento(pago[1])
                if nombreCliente == None:
                    nombreCliente = ["N/A", "N/A", "N/A"]
                for j, campo in enumerate(pago):
                    item = QTableWidgetItem(str(campo))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(0, 0, 0))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    tablaPagos.setItem(i, j, item)
                nombreCliente = f"{nombreCliente[0]} {nombreCliente[1]} {nombreCliente[2]}"
                tablaPagos.setItem(i, 6, QTableWidgetItem(nombreCliente))
            tablaPagos.itemClicked.connect(self.pagoClicado)
        tablaPagos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def pagoClicado(self, item):
        row = item.row()
        idRenglon = item.tableWidget().item(row, 0).text()
        
        # Obtener información del pago seleccionado y la opción de finalizar el pago en caso de estar pendiente
        pago = self.db.consultar_Pago(idRenglon)
        self.mensaje = QMessageBox(self)
        self.mensaje.setWindowTitle("Información del pago")
        self.mensaje.setText(f"""Numero: {pago[0]}\nNo. Evento: {pago[1]}\nMonto: {pago[2]}\nFecha Inicial: {pago[3]}\nPago Inicial: {pago[4]}\n Estado: {"Inpago" if pago[5] == None else "Pagado"}""")
        
        finalizar = None
        if pago[5] == None:
            finalizar = self.mensaje.addButton("Finalizar", QMessageBox.AcceptRole)
        
        cerrar = self.mensaje.addButton("Cerrar", QMessageBox.RejectRole)
        
        self.mensaje.exec_()
        
        if self.mensaje.clickedButton() == finalizar:
            self.finalizar_pago(pago)

    def finalizar_pago(self, pago):
        # Finaliza el pago seleccionado
        self.db.finalizar_Pago(pago[0])
    
    def ventana_eventos_pagados(self):
        # Limpiar el diseño lateral derecho
        self.limpiar()
        
        # Añadir nuevo contenido para la interfaz de eventos pagados
        tablaPagos = QTableWidget()
        tablaPagos.setColumnCount(7)
        tablaPagos.setEditTriggers(QTableWidget.NoEditTriggers)
        tablaPagos.setSelectionBehavior(QTableWidget.SelectRows)
        tablaPagos.verticalHeader().setVisible(False)
        tablaPagos.setHorizontalHeaderLabels(["No.", "Fecha", "Descripción", "Nombres", "Monto", "Fecha saldada", "Servicios"])
        tablaPagos.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.diseño_derecho.addWidget(tablaPagos)

        # Insersión de los pagos en la tabla obtenidos de la base de datos
        pagos = self.db.consultar_eventos_pagados()
        if pagos:
            tablaPagos.setRowCount(len(pagos))
            for i, pago in enumerate(pagos):
                nombreCliente = self.db.consultar_Cliente_porEvento(pago[1])
                if nombreCliente == None:
                    nombreCliente = ["N/A", "N/A", "N/A"]
                for j, campo in enumerate(pago):
                    if campo == None:
                        campo = "N/A"
                    item = QTableWidgetItem(str(campo))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(0, 0, 0))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    tablaPagos.setItem(i, j, item)
            tablaPagos.itemClicked.connect(self.eventoClicadoPagado)
        tablaPagos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def eventoClicadoPagado(self, item):
        row = item.row()
        idRenglon = item.tableWidget().item(row, 0).text()
        detalles = []

        for col in range(item.tableWidget().columnCount()):
            detalles.append(item.tableWidget().item(row, col).text())
        
        # Obtener información del evento seleccionado
        evento = list(self.db.consultar_evento_detallado(idRenglon))
        mensaje = QMessageBox(self)
        mensaje.setWindowTitle("Información del evento")

        for i in range(len(evento)):
            if evento[i] == None:
                evento[i] = "N/A"

        mensaje.setText(f"""Numero: {evento[0]}\n Fecha: {evento[1]}\nCliente: {evento[2]} {evento[3]} {evento[4]}\nTeléfono: {evento[5]}\nSalón: {evento[6]},\n\nInformación adicional: {evento[7]}""")
        cerrar = mensaje.addButton("Cerrar", QMessageBox.RejectRole)
        imprimirbt = mensaje.addButton("Imprimir", QMessageBox.AcceptRole)
        imprimirbt.clicked.connect(lambda: self.imprimirPagado(detalles))
        
        mensaje.exec_()

    def imprimirPagado(self, evento):
        # Imprime un PDF con la información del evento seleccionado
        self.pdf = pdf()
        self.pdf.agregar_evento_pagado(evento)

    def limpiar(self):
        # Limpiar el diseño lateral derecho
        for i in reversed(range(self.diseño_derecho.count())):
            widget = self.diseño_derecho.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
            
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Recepcion()
    window.show()
    sys.exit(app.exec())