import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout,QHBoxLayout,QPushButton,QScrollArea,QTableWidget,QLineEdit,QTableWidgetItem, QLabel, QMainWindow, QMessageBox, QComboBox, QDialog, QDateEdit, QHeaderView
from PySide6.QtGui import QFont, QPixmap, QColor
from PySide6.QtCore import Qt
from GeneradorPDF import GeneradorPDF as pdf


class VentanaPrincipal(QMainWindow):
    def __init__(self, nombre, bd):
        super().__init__()
        self.db = bd

        self.setWindowTitle(f"Organizador. Bienvenido {nombre[1]} {nombre[2]}") 
        self.resize(700, 400)
        widget = QWidget()
        
        # Crear diseño para el menú lateral izquierdo
        diseño_lateral_izquierdo = QVBoxLayout()
        
        self.boton_eventos = QPushButton("Eventos")
        self.boton_eventos.setStyleSheet("background-color: #FF7E67; color: white;")
        self.boton_eventos.clicked.connect(self.interfazEventos)
        diseño_lateral_izquierdo.addWidget(self.boton_eventos)
        
        self.boton_salones = QPushButton("Salones")
        self.boton_salones.setStyleSheet("background-color: #FF7E67; color: white;")
        self.boton_salones.clicked.connect(self.interfazSalones)
        diseño_lateral_izquierdo.addWidget(self.boton_salones)
        
        self.boton_pagos = QPushButton("Pagos")
        self.boton_pagos.setStyleSheet("background-color: #FF7E67; color: white;")
        self.boton_pagos.clicked.connect(self.interfazPagos)
        diseño_lateral_izquierdo.addWidget(self.boton_pagos)
        
        self.boton_proveedores = QPushButton("Proveedores")
        self.boton_proveedores.setStyleSheet("background-color: #FF7E67; color: white;")
        self.boton_proveedores.clicked.connect(self.interfazProveedores)
        diseño_lateral_izquierdo.addWidget(self.boton_proveedores)
        
        self.boton_servicios_evento = QPushButton("Servicios Evento")
        self.boton_servicios_evento.setStyleSheet("background-color: #FF7E67; color: white;")
        self.boton_servicios_evento.clicked.connect(self.interfazServiciosEvento)
        diseño_lateral_izquierdo.addWidget(self.boton_servicios_evento)

        self.boton_eventos_pagados = QPushButton("Eventos Pagados")
        self.boton_eventos_pagados.setStyleSheet("background-color: #FF7E67; color: white;")
        self.boton_eventos_pagados.clicked.connect(self.ventana_eventos_pagados)
        diseño_lateral_izquierdo.addWidget(self.boton_eventos_pagados)
        
        # Diseño de bienvenida
        icono_usuario = QLabel()
        icono_usuario.setPixmap(QPixmap("UsuarioIcon.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        bienvenidaLabel = QLabel(f"¡Bienvenido {nombre[1]} {nombre[2]}!")
        bienvenidaLabel.setFont(QFont("Arial", 20))
        bienvenidaLabel.setContentsMargins(0, 0, 0, 0)
        bienvenidaLabel.setAlignment(Qt.AlignCenter)

        # Crear diseño para el contenido del lado derecho
        self.diseño_lateral_derecho = QVBoxLayout()
        self.diseño_lateral_derecho.addWidget(icono_usuario, alignment=Qt.AlignCenter)
        self.diseño_lateral_derecho.addWidget(bienvenidaLabel)

        # Crear diseño principal
        diseño_principal = QHBoxLayout()
        diseño_principal.addLayout(diseño_lateral_izquierdo)
        diseño_principal.addLayout(self.diseño_lateral_derecho)

        widget.setLayout(diseño_principal)
        self.setCentralWidget(widget)
        
    def interfazEventos(self):
        """Esta función actualiza toda la interfaz para mostrar los eventos en pantalla
        """
        self.limpiar_diseño(self.diseño_lateral_derecho)

        # Añadir botones
        diseño_botones = QHBoxLayout()
        self.boton_añadir = QPushButton("Añadir")
        self.boton_añadir.setStyleSheet("background-color: #FF7E67; color: white;")
        self.boton_eliminar = QPushButton("Eliminar")

        diseño_botones.addWidget(self.boton_añadir)
        diseño_botones.addWidget(self.boton_eliminar)
        self.diseño_lateral_derecho.addLayout(diseño_botones)
        
        # Añadir nuevo contenido para la interfaz de eventos
        self.boton_añadir.clicked.connect(self.anadirEvento)
        self.boton_añadir.clicked.connect(lambda: self.boton_añadir.clicked.disconnect())
        # self.boton_eliminar.clicked.connect(self.eliminarEvento)

        buscarProovedor = QLineEdit()
        buscarProovedor.setPlaceholderText("Datos del proveedor aquí")
        
        mostrarProovedor = QTableWidget()
        mostrarProovedor.setColumnCount(6)
        mostrarProovedor.verticalHeader().setVisible(False)
        mostrarProovedor.setEditTriggers(QTableWidget.NoEditTriggers)
        mostrarProovedor.setSelectionBehavior(QTableWidget.SelectRows)
        mostrarProovedor.setHorizontalHeaderLabels(["No.", "Fecha", "Descripción", "Nombres", "Total", "Anticipo"])
        mostrarProovedor.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        mostrarProovedor.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

        area_desplazamiento = QScrollArea()
        area_desplazamiento.setWidgetResizable(True)
        area_desplazamiento.setWidget(mostrarProovedor)
        self.diseño_lateral_derecho.addWidget(area_desplazamiento)
        
        # Insersión de los eventos en la tabla obtenidos de la base de datos
        eventos = self.db.consultar_eventos_no_pagados()
        
        if eventos:
            mostrarProovedor.setRowCount(len(eventos))
            for i, evento in enumerate(eventos):
                for j, campo in enumerate(evento):
                    item = QTableWidgetItem(str(campo))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(0, 0, 0))
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
        
        mensaje.exec_()

    def anadirEvento(self):
        # Ventana para añadir un evento
        self.resize(700, 500)
        fecha = QDateEdit()
        fecha.setDisplayFormat("yyyy/MM/dd")
        descripcion = QLineEdit()
        descripcion.setPlaceholderText("Descripción del evento")
        cliente_label = QLabel("Cliente:")
        cliente_combo = QComboBox()
        clientes = self.db.consultar_Clientes()
        for cliente in clientes:
            cliente_combo.addItem(f"{cliente[1]} {cliente[2]} {cliente[0]}")
        
        añadir_cliente_boton = QPushButton("Añadir Cliente")
        añadir_cliente_boton.setStyleSheet("background-color: #FF7E67; color: white;")
        añadir_cliente_boton.clicked.connect(self.anadirCliente)

        salonCombo = QComboBox()
        salones = self.db.consultar_Salones()
        for salon in salones:
            salonCombo.addItem(salon[1])

        precioTotal = QLineEdit()
        precioTotal.setPlaceholderText("Precio total")
        anticipo = QLineEdit()
        anticipo.setPlaceholderText("Anticipo")
        
        aceptar_boton = QPushButton("Aceptar")
        aceptar_boton.setStyleSheet("background-color: #FF7E67; color: white;")
        aceptar_boton.clicked.connect(lambda: self.db.insertar_evento(anticipo.text() ,precioTotal.text() ,(fecha.text()), descripcion.text(), cliente_combo.currentText()[-1], salonCombo.currentText()))
        aceptar_boton.clicked.connect(lambda: QMessageBox.information(self, "Evento añadido", "Evento añadido"))
        aceptar_boton.clicked.connect(lambda: self.limpiar_diseño(self.layoutEvento))
        aceptar_boton.clicked.connect(lambda: self.interfazEventos())

        self.layoutEvento = QVBoxLayout()
        self.layoutEvento.addWidget(cliente_label)
        self.layoutEvento.addWidget(cliente_combo)
        self.layoutEvento.addWidget(añadir_cliente_boton)
        self.layoutEvento.addWidget(fecha)
        self.layoutEvento.addWidget(descripcion)
        self.layoutEvento.addWidget(salonCombo)
        self.layoutEvento.addWidget(precioTotal)
        self.layoutEvento.addWidget(anticipo)
        self.layoutEvento.addWidget(aceptar_boton)
        
        self.diseño_lateral_derecho.addLayout(self.layoutEvento)        

    def anadirCliente(self):
        # Ventana para añadir un cliente
        QDIalog = QDialog()
        nombre_cliente = QLineEdit()
        nombre_cliente.setPlaceholderText("Nombre del cliente")
        apellido_paterno = QLineEdit()
        apellido_paterno.setPlaceholderText("Apellido paterno")
        apellido_materno = QLineEdit()
        apellido_materno.setPlaceholderText("Apellido materno")
        telefono_cliente = QLineEdit()
        telefono_cliente.setPlaceholderText("Teléfono del cliente")

        layout = QVBoxLayout()
        layout.addWidget(nombre_cliente)
        layout.addWidget(apellido_paterno)
        layout.addWidget(apellido_materno)
        layout.addWidget(telefono_cliente)
        boton = QPushButton("Añadir")
        boton.clicked.connect(lambda: self.db.insertar_Cliente(nombre_cliente.text(), apellido_paterno.text(), apellido_materno.text(), telefono_cliente.text()))
        boton.clicked.connect(lambda: QMessageBox.information(self, "Cliente añadido", "Cliente añadido"))
        boton.clicked.connect(lambda: self.eliminarLayout(layout))
        boton.clicked.connect(lambda: self.eliminarLayout(self.layoutEvento))
        boton.clicked.connect(lambda: self.eliminarLayout(self.interfazEventos()))
        boton.clicked.connect(QDIalog.close)
        layout.addWidget(boton)
        QDIalog.setLayout(layout)
        QDIalog.exec()
    
    def limpiar_diseño(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.limpiar_diseño(item.layout())

    
    def interfazSalones(self):
        """Esta función actualiza toda la interfaz para mostrar los salones en pantalla
        """
        self.limpiar_diseño(self.diseño_lateral_derecho)
        
        # Añadir nuevo contenido para la interfaz de salones
        layuot_salones = QVBoxLayout()
        etiqueta_salones = QLabel("Salones")
        etiqueta_salones.setAlignment(Qt.AlignCenter)
        
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
            layuot_salones.addWidget(etiqueta_salones)
            layuot_salones.addWidget(area_desplazamiento)
            self.diseño_lateral_derecho.addLayout(layuot_salones)
        else:
            etiqueta_salones.setText("No hay salones")
            layuot_salones.addWidget(etiqueta_salones)
        
    def interfazPagos(self):
        """Esta función actualiza toda la interfaz para mostrar los pagos en pantalla
        """
        self.limpiar_diseño(self.diseño_lateral_derecho)
                
        # Añadir nuevo contenido para la interfaz de pagos
        botonPagar = QPushButton("Pagar")
        botonPagar.setStyleSheet("background-color: #FF7E67; color: white;")
        self.diseño_lateral_derecho.addWidget(botonPagar)
        
        # Interfaz de pagos
        tablaPagos = QTableWidget()
        tablaPagos.setColumnCount(7)
        tablaPagos.setEditTriggers(QTableWidget.NoEditTriggers)
        tablaPagos.setSelectionBehavior(QTableWidget.SelectRows)
        tablaPagos.verticalHeader().setVisible(False)
        tablaPagos.setHorizontalHeaderLabels(["No.", "No. Evento", "P.I", "Fecha", "Fecha", "Estado", "Cliente"])
        self.diseño_lateral_derecho.addWidget(tablaPagos)

        # Insersión de los pagos en la tabla obtenidos de la base de datos
        pagos = self.db.consultar_Pagos()
        if pagos:
            tablaPagos.setRowCount(len(pagos))
            for i, pago in enumerate(pagos):
                nombreCliente = self.db.consultar_Cliente_porEvento(pago[1])
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
        cerrar = self.mensaje.addButton("Cerrar", QMessageBox.RejectRole)
        
        self.mensaje.exec_()

    def interfazProveedores(self):
        """Esta función actualiza toda la interfaz para mostrar los proveedores en pantalla
        """
        self.limpiar_diseño(self.diseño_lateral_derecho)
            
        # Añadir nuevo contenido para la interfaz de proveedores
        etiqueta_proveedores = QLabel("Proveedores")
        etiqueta_proveedores.setAlignment(Qt.AlignCenter)
        self.diseño_lateral_derecho.addWidget(etiqueta_proveedores)

        # Botones para añadir y eliminar proveedores
        boton_añadir_proveedor = QPushButton("Añadir")
        boton_añadir_proveedor.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_añadir_proveedor.clicked.connect(self.anadirProveedor)
        self.diseño_lateral_derecho.addWidget(boton_añadir_proveedor)

        proveedores = self.db.consultar_Proveedores()
        if proveedores:
            tabla_proveedores = QTableWidget()
            tabla_proveedores.setColumnCount(3)
            tabla_proveedores.verticalHeader().setVisible(False)
            tabla_proveedores.setEditTriggers(QTableWidget.NoEditTriggers)
            tabla_proveedores.setSelectionBehavior(QTableWidget.SelectRows)
            tabla_proveedores.setHorizontalHeaderLabels(["No.", "Proveedor", "Correo", "Servicio"])
            tabla_proveedores.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
            tabla_proveedores.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            tabla_proveedores.verticalHeader().setVisible(False)
            
            tabla_proveedores.setRowCount(len(proveedores))
            for i, proveedor in enumerate(proveedores):
                for j, campo in enumerate(proveedor):
                    item = QTableWidgetItem(str(campo))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(0, 0, 0))
                    tabla_proveedores.setItem(i, j, item)
            
            area_desplazamiento = QScrollArea()
            area_desplazamiento.setWidgetResizable(True)
            area_desplazamiento.setWidget(tabla_proveedores)
            self.diseño_lateral_derecho.addWidget(area_desplazamiento)
        else:
            etiqueta_proveedores.setText("No hay proveedores")
            self.diseño_lateral_derecho.addWidget(etiqueta_proveedores)

    def anadirProveedor(self):
        # Ventana para añadir un proveedor
        QDIalog = QDialog()
        nombre_proveedor = QLineEdit()
        nombre_proveedor.setPlaceholderText("Nombre del proveedor")
        correo_proveedor = QLineEdit()
        correo_proveedor.setPlaceholderText("Correo del proveedor")
        servicio_proveedor = QLineEdit()
        servicio_proveedor.setPlaceholderText("Servicio del proveedor")

        layout = QVBoxLayout()
        layout.addWidget(nombre_proveedor)
        layout.addWidget(correo_proveedor)
        layout.addWidget(servicio_proveedor)
        boton = QPushButton("Añadir")
        boton.clicked.connect(lambda: self.db.insertar_Proveedor(nombre_proveedor.text(), correo_proveedor.text(), servicio_proveedor.text()))
        boton.clicked.connect(lambda: QMessageBox.information(self, "Proveedor añadido", "Proveedor añadido"))
        boton.clicked.connect(lambda: self.eliminarLayout(layout))
        boton.clicked.connect(lambda: self.interfazProveedores())
        boton.clicked.connect(QDIalog.close)
        layout.addWidget(boton)
        QDIalog.setLayout(layout)
        QDIalog.exec()

    def interfazServiciosEvento(self):
        """Esta función actualiza toda la interfaz para mostrar los servicios de eventos en pantalla
        """
        self.limpiar_diseño(self.diseño_lateral_derecho)
        
        # Añadir nuevo contenido para la interfaz de servicios de eventos
        etiqueta_servicios_evento = QLabel("Servicios de Evento")
        etiqueta_servicios_evento.setAlignment(Qt.AlignCenter)
        self.diseño_lateral_derecho.addWidget(etiqueta_servicios_evento)

        # Botones para añadir y eliminar servicios de eventos
        boton_añadir_servicio = QPushButton("Añadir")
        boton_añadir_servicio.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_añadir_servicio.clicked.connect(self.anadirServicio)
        self.diseño_lateral_derecho.addWidget(boton_añadir_servicio)

        imprimir_servicios = QPushButton("Imprimir")
        imprimir_servicios.setStyleSheet("background-color: #FF7E67; color: white;")
        imprimir_servicios.clicked.connect(self.imprimirServicios)
        self.diseño_lateral_derecho.addWidget(imprimir_servicios)

        servicios = self.db.consultar_servicios()
        if servicios:
            tabla_servicios = QTableWidget()
            tabla_servicios.setColumnCount(4)
            tabla_servicios.verticalHeader().setVisible(False)
            tabla_servicios.setEditTriggers(QTableWidget.NoEditTriggers)
            tabla_servicios.setSelectionBehavior(QTableWidget.SelectRows)
            tabla_servicios.setHorizontalHeaderLabels(["No.", "Servicio", "Descripción", "Telefono"])
            tabla_servicios.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
            tabla_servicios.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            tabla_servicios.verticalHeader().setVisible(False)
            
            tabla_servicios.setRowCount(len(servicios))
            for i, servicio in enumerate(servicios):
                for j, campo in enumerate(servicio):
                    item = QTableWidgetItem(str(campo))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(0, 0, 0))
                    tabla_servicios.setItem(i, j, item)
            
            area_desplazamiento = QScrollArea()
            area_desplazamiento.setWidgetResizable(True)
            area_desplazamiento.setWidget(tabla_servicios)
            self.diseño_lateral_derecho.addWidget(area_desplazamiento)
        else:
            etiqueta_servicios_evento.setText("No hay servicios de eventos")
            self.diseño_lateral_derecho.addWidget(etiqueta_servicios_evento)
    
    def imprimirServicios(self):
        # Imprimir los servicios de eventos en un PDF
        servicios = self.db.consultar_servicios()
        if servicios:
            pdfServicios = pdf("Servicios.pdf")
            pdfServicios.agregar_servicios(servicios)
    
    def anadirServicio(self):
        # Ventana para añadir un servicio
        QDIalog = QDialog()
        nombre_servicio = QLineEdit()
        nombre_servicio.setPlaceholderText("Nombre del servicio")
        descripcion_servicio = QLineEdit()
        descripcion_servicio.setPlaceholderText("Descripción del servicio")
        telefono_servicio = QLineEdit()
        telefono_servicio.setPlaceholderText("Teléfono del servicio")

        layout = QVBoxLayout()
        layout.addWidget(nombre_servicio)
        layout.addWidget(descripcion_servicio)
        layout.addWidget(telefono_servicio)
        boton = QPushButton("Añadir")
        boton.clicked.connect(lambda: self.db.insertar_Servicio(nombre_servicio.text(), descripcion_servicio.text(), telefono_servicio.text()))
        boton.clicked.connect(lambda: QMessageBox.information(self, "Servicio añadido", "Servicio añadido"))
        boton.clicked.connect(lambda: self.eliminarLayout(layout))
        boton.clicked.connect(lambda: self.interfazServiciosEvento())
        boton.clicked.connect(QDIalog.close)
        layout.addWidget(boton)
        QDIalog.setLayout(layout)
        QDIalog.exec()


    
    def ventana_eventos_pagados(self):
        # Limpiar el diseño lateral derecho
        self.limpiar_diseño(self.diseño_lateral_derecho)
        
        # Añadir nuevo contenido para la interfaz de eventos pagados
        tablaPagos = QTableWidget()
        tablaPagos.setColumnCount(6)
        tablaPagos.setEditTriggers(QTableWidget.NoEditTriggers)
        tablaPagos.setSelectionBehavior(QTableWidget.SelectRows)
        tablaPagos.verticalHeader().setVisible(False)
        tablaPagos.setHorizontalHeaderLabels(["No.", "Fecha", "Descripción", "Nombres", "Monto", "Fecha saldada"])
        tablaPagos.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.diseño_lateral_derecho.addWidget(tablaPagos)

        # Insersión de los pagos en la tabla obtenidos de la base de datos
        pagos = self.db.consultar_eventos_pagados()
        if pagos:
            tablaPagos.setRowCount(len(pagos))
            for i, pago in enumerate(pagos):
                nombreCliente = self.db.consultar_Cliente_porEvento(pago[1])
                for j, campo in enumerate(pago):
                    item = QTableWidgetItem(str(campo))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(0, 0, 0))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    tablaPagos.setItem(i, j, item)
            tablaPagos.itemClicked.connect(self.eventoClicado)
        tablaPagos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())