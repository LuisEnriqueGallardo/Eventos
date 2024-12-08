from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QScrollArea, QHBoxLayout, QVBoxLayout, QMainWindow, QWidget
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton

class VentanaAdmin(QMainWindow):
    def __init__(self, nombre, bd):
        super().__init__()
        self.db = bd
        
        self.setWindowTitle(f"Administrador. Bienvenido {nombre[1]} {nombre[2]}")
        self.resize(700, 400)
        widget = QWidget()
        
        # Crear diseño para el menú lateral izquierdo
        diseño_lateral_izquierdo = QVBoxLayout()
        
        boton_clientes = QPushButton("Clientes")
        boton_clientes.setStyleSheet("background-color: #FF7E67; color: white;")
        diseño_lateral_izquierdo.addWidget(boton_clientes)
        
        boton_eventos = QPushButton("Eventos")
        boton_eventos.setStyleSheet("background-color: #FF7E67; color: white;")
        diseño_lateral_izquierdo.addWidget(boton_eventos)
        
        boton_empleados = QPushButton("Empleados")
        boton_empleados.setStyleSheet("background-color: #FF7E67; color: white;")
        diseño_lateral_izquierdo.addWidget(boton_empleados)
        
        boton_salones = QPushButton("Salones")
        boton_salones.setStyleSheet("background-color: #FF7E67; color: white;")
        diseño_lateral_izquierdo.addWidget(boton_salones)
        
        boton_pagos = QPushButton("Pagos")
        boton_pagos.setStyleSheet("background-color: #FF7E67; color: white;")
        diseño_lateral_izquierdo.addWidget(boton_pagos)
        
        boton_proveedores = QPushButton("Proveedores")
        boton_proveedores.setStyleSheet("background-color: #FF7E67; color: white;")
        diseño_lateral_izquierdo.addWidget(boton_proveedores)
        
        boton_organizadores = QPushButton("Organizadores")
        boton_organizadores.setStyleSheet("background-color: #FF7E67; color: white;")
        diseño_lateral_izquierdo.addWidget(boton_organizadores)
        
        boton_servicios_evento = QPushButton("Servicios Evento")
        boton_servicios_evento.setStyleSheet("background-color: #FF7E67; color: white;")
        diseño_lateral_izquierdo.addWidget(boton_servicios_evento)
        
        # Crear diseño para el contenido del lado derecho
        diseño_lateral_derecho = QVBoxLayout()
        
        # Añadir botones
        diseño_botones = QVBoxLayout()
        boton_añadir = QPushButton("Añadir")
        boton_eliminar = QPushButton("Eliminar")
        boton_añadir.setStyleSheet("background-color: #FF7E67; color: white;")

        diseño_botones.addWidget(boton_añadir)
        diseño_botones.addWidget(boton_eliminar)
        diseño_lateral_derecho.addLayout(diseño_botones)
        
        # Crear layout principal
        layout_principal = QHBoxLayout()
        layout_principal.addLayout(diseño_lateral_izquierdo)
        layout_principal.addLayout(diseño_lateral_derecho)
        
        widget.setLayout(layout_principal)
        self.setCentralWidget(widget)
         
    def interfazEventos(self):
        # Limpiar el diseño lateral derecho
        for i in reversed(range(self.diseño_lateral_derecho.count())):
            widget_to_remove = self.diseño_lateral_derecho.itemAt(i).widget()
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
        self.diseño_lateral_derecho.addWidget(area_desplazamiento)
        
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
                    mostrarProovedor.setItem(i, j, item)
        else:
            mostrarProovedor.setRowCount(1)
            mostrarProovedor.setItem(0, 0, QTableWidgetItem("No hay eventos"))
            mostrarProovedor.setColumnCount(1)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaAdmin()
    ventana.show()
    app.exec()