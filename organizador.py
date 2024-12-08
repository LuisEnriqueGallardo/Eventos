import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout,QHBoxLayout,QPushButton,QScrollArea,QTableWidget,QLineEdit,QTableWidgetItem, QLabel, QMainWindow
from PySide6.QtGui import QFont, QPixmap, QColor
from PySide6.QtCore import Qt

class VentanaPrincipal(QMainWindow):
    def __init__(self, nombre, bd):
        super().__init__()
        self.db = bd

        self.setWindowTitle(f"Organizador. Bienvenido {nombre[1]} {nombre[2]}") 
        self.resize(700, 400)
        widget = QWidget()
        
        # Crear diseño para el menú lateral izquierdo
        diseño_lateral_izquierdo = QVBoxLayout()
        
        boton_eventos = QPushButton("Eventos")
        boton_eventos.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_eventos.clicked.connect(self.interfazEventos)
        diseño_lateral_izquierdo.addWidget(boton_eventos)
        
        boton_salones = QPushButton("Salones")
        boton_salones.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_salones.clicked.connect(self.interfazSalones)
        diseño_lateral_izquierdo.addWidget(boton_salones)
        
        boton_pagos = QPushButton("Pagos")
        boton_pagos.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_pagos.clicked.connect(self.interfazPagos)
        diseño_lateral_izquierdo.addWidget(boton_pagos)
        
        boton_proveedores = QPushButton("Proveedores")
        boton_proveedores.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_proveedores.clicked.connect(self.interfazProveedores)
        diseño_lateral_izquierdo.addWidget(boton_proveedores)
        
        boton_servicios_evento = QPushButton("Servicios Evento")
        boton_servicios_evento.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_servicios_evento.clicked.connect(self.interfazServiciosEvento)
        diseño_lateral_izquierdo.addWidget(boton_servicios_evento)
        
        # Diseño de bienvenida
        icono_usuario = QLabel()
        icono_usuario.setPixmap(QPixmap("UsuarioIcon.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        bienvenidaLabel = QLabel(f"¡Bienvenido {nombre[1]} {nombre[2]}!")
        bienvenidaLabel.setFont(QFont("Arial", 20))
        bienvenidaLabel.setContentsMargins(0, 0, 0, 0)
        bienvenidaLabel.setAlignment(Qt.AlignCenter)

        # Añadir botones
        diseño_botones = QHBoxLayout()
        boton_añadir = QPushButton("Añadir")
        boton_añadir.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_eliminar = QPushButton("Eliminar")

        # Crear diseño para el contenido del lado derecho
        self.diseño_lateral_derecho = QVBoxLayout()
        self.diseño_lateral_derecho.addWidget(icono_usuario, alignment=Qt.AlignCenter)
        self.diseño_lateral_derecho.addWidget(bienvenidaLabel)

        diseño_botones.addWidget(boton_añadir)
        diseño_botones.addWidget(boton_eliminar)
        self.diseño_lateral_derecho.addLayout(diseño_botones)

        # Crear diseño principal
        diseño_principal = QHBoxLayout()
        diseño_principal.addLayout(diseño_lateral_izquierdo)
        diseño_principal.addLayout(self.diseño_lateral_derecho)

        widget.setLayout(diseño_principal)
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
    
    def interfazSalones(self):
        """Esta función actualiza toda la interfaz para mostrar los salones en pantalla
        """
        # Limpiar el diseño lateral derecho
        for i in reversed(range(self.layout().itemAt(1).count())):
            widget_to_remove = self.layout().itemAt(1).itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)
        
        # Añadir nuevo contenido para la interfaz de salones
        etiqueta_salones = QLabel("Salones")
        etiqueta_salones.setAlignment(Qt.AlignCenter)
        self.layout().itemAt(1).addWidget(etiqueta_salones)
        
        # Obtener los salones de la base de datos
        salones = self.db.consultar_Salones()
        if salones:
            tabla_salones = QTableWidget()
            tabla_salones.setColumnCount(2)
            tabla_salones.verticalHeader().setVisible(False)
            tabla_salones.setEditTriggers(QTableWidget.NoEditTriggers)
            tabla_salones.setSelectionBehavior(QTableWidget.SelectRows)
            tabla_salones.setHorizontalHeaderLabels(["ID", "Salón"])
            tabla_salones.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
            
            tabla_salones.setRowCount(len(salones))
            for i, salon in enumerate(salones):
                for j, campo in enumerate(salon):
                    item = QTableWidgetItem(str(campo))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(0, 0, 0))
                    tabla_salones.setItem(i, j, item)
            
            area_desplazamiento = QScrollArea()
            area_desplazamiento.setWidgetResizable(True)
            area_desplazamiento.setWidget(tabla_salones)
            self.layout().itemAt(1).addWidget(area_desplazamiento)
        
    def interfazPagos(self):
        """Esta función actualiza toda la interfaz para mostrar los pagos en pantalla
        """
        # Limpiar el diseño lateral derecho
        for i in reversed(range(self.layout().itemAt(1).count())):
            widget_to_remove = self.layout().itemAt(1).itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)
        
        # Añadir nuevo contenido para la interfaz de pagos
        etiqueta_pagos = QLabel("Pagos")
        etiqueta_pagos.setAlignment(Qt.AlignCenter)
        self.layout().itemAt(1).addWidget(etiqueta_pagos)
        
    def interfazProveedores(self):
        """Esta función actualiza toda la interfaz para mostrar los proveedores en pantalla
        """
        # Limpiar el diseño lateral derecho
        for i in reversed(range(self.layout().itemAt(1).count())):
            widget_to_remove = self.layout().itemAt(1).itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)
        
        # Añadir nuevo contenido para la interfaz de proveedores
        etiqueta_proveedores = QLabel("Proveedores")
        etiqueta_proveedores.setAlignment(Qt.AlignCenter)
        self.layout().itemAt(1).addWidget(etiqueta_proveedores)
        
    def interfazServiciosEvento(self):
        """Esta función actualiza toda la interfaz para mostrar los servicios de eventos en pantalla
        """
        # Limpiar el diseño lateral derecho
        for i in reversed(range(self.layout().itemAt(1).count())):
            widget_to_remove = self.layout().itemAt(1).itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)
        
        # Añadir nuevo contenido para la interfaz de servicios de eventos
        etiqueta_servicios_evento = QLabel("Servicios de Evento")
        etiqueta_servicios_evento.setAlignment(Qt.AlignCenter)
        self.layout().itemAt(1).addWidget(etiqueta_servicios_evento)
        
if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())