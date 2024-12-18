from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLineEdit, QTableWidget, QTableWidgetItem, QScrollArea, QHBoxLayout, QVBoxLayout, QMainWindow, QWidget, QMessageBox, QDialog, QHeaderView, QLabel, QComboBox
from PySide6.QtGui import QColor, QPixmap, QFont
from PySide6.QtWidgets import QPushButton
from GeneradorPDF import GeneradorPDF as pdf


class VentanaAdmin(QMainWindow):
    def __init__(self, nombre, bd):
        super().__init__()
        self.db = bd
        self.nombre = nombre
        
        self.setWindowTitle(f"Administrador. Bienvenido {nombre[1]} {nombre[2]}")
        self.resize(700, 400)
        widget = QWidget()
        
        # Crear diseño para el menú lateral izquierdo
        diseño_lateral_izquierdo = QVBoxLayout()
        
        boton_clientes = QPushButton("Clientes")
        boton_clientes.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_clientes.clicked.connect(self.interfazClientes)
        diseño_lateral_izquierdo.addWidget(boton_clientes)
        
        boton_eventos = QPushButton("Eventos")
        boton_eventos.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_eventos.clicked.connect(self.interfazEventos)
        diseño_lateral_izquierdo.addWidget(boton_eventos)
        
        boton_empleados = QPushButton("Empleados")
        boton_empleados.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_empleados.clicked.connect(self.interfazEmpleados)
        diseño_lateral_izquierdo.addWidget(boton_empleados)
        
        boton_salones = QPushButton("Salones")
        boton_salones.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_salones.clicked.connect(self.interfazSalones)
        diseño_lateral_izquierdo.addWidget(boton_salones)
        
        boton_pagos = QPushButton("Pagos")
        boton_pagos.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_pagos.clicked.connect(self.ventanaPagos)
        diseño_lateral_izquierdo.addWidget(boton_pagos)
        
        boton_proveedores = QPushButton("Proveedores")
        boton_proveedores.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_proveedores.clicked.connect(self.interfazProveedores)
        diseño_lateral_izquierdo.addWidget(boton_proveedores)
        
        boton_servicios_evento = QPushButton("Servicios Evento")
        boton_servicios_evento.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_servicios_evento.clicked.connect(self.interfazServiciosEvento)
        diseño_lateral_izquierdo.addWidget(boton_servicios_evento)

        boton_eventos_pagados = QPushButton("Eventos Pagados")
        boton_eventos_pagados.setStyleSheet("background-color: #FF7E67; color: white;")
        boton_eventos_pagados.clicked.connect(self.ventana_eventos_pagados)
        diseño_lateral_izquierdo.addWidget(boton_eventos_pagados)

        # Crear diseño para el contenido del lado derecho
        self.diseño_lateral_derecho = QVBoxLayout()

        # Elementos centrales
        icono_usuario = QLabel()
        icono_usuario.setPixmap(QPixmap("UsuarioIcon.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        bienvenidaLabel = QLabel("¡Bienvenido!")
        bienvenidaLabel.setFont(QFont("Arial", 20))
        bienvenidaLabel.setContentsMargins(0, 0, 0, 0)
        
        nombreUsuario = QLabel(f"{nombre[1]} {nombre[2]}")
        nombreUsuario.setFont(QFont("Arial", 15))
        nombreUsuario.setContentsMargins(0, 0, 0, 0)
        
        self.diseño_lateral_derecho.insertWidget(0, icono_usuario, 0, Qt.AlignCenter)
        self.diseño_lateral_derecho.insertWidget(1, bienvenidaLabel, 0, Qt.AlignCenter)
        self.diseño_lateral_derecho.insertWidget(2, nombreUsuario, 0, Qt.AlignCenter)
        
        
        # Crear layout principal
        layout_principal = QHBoxLayout()
        layout_principal.addLayout(diseño_lateral_izquierdo)
        layout_principal.addLayout(self.diseño_lateral_derecho)
        
        widget.setLayout(layout_principal)
        self.setCentralWidget(widget)

    def interfazClientes(self):
        # Limpiar el diseño lateral derecho
        self.limpiar_diseño(self.diseño_lateral_derecho)

        # Añadir botones
        diseño_botones = QVBoxLayout()
        boton_añadir = QPushButton("Añadir")
        boton_añadir.clicked.connect(self.anadirCliente)
        boton_añadir.setStyleSheet("background-color: #FF7E67; color: white;")

        diseño_botones.addWidget(boton_añadir)
        self.diseño_lateral_derecho.addLayout(diseño_botones)
        
        # Añadir nuevo contenido para la interfaz de clientes
        buscarCliente = QLineEdit()
        buscarCliente.setPlaceholderText("Datos del cliente aquí")
        
        mostrarCliente = QTableWidget()
        mostrarCliente.setColumnCount(5)
        mostrarCliente.verticalHeader().setVisible(False)
        mostrarCliente.setEditTriggers(QTableWidget.NoEditTriggers)
        mostrarCliente.setSelectionBehavior(QTableWidget.SelectRows)
        mostrarCliente.setHorizontalHeaderLabels(["No.", "Nombre(s)", "Apellido P.", "Apellido M.", "Telefono"])
        mostrarCliente.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

        area_desplazamiento = QScrollArea()
        area_desplazamiento.setWidgetResizable(True)
        area_desplazamiento.setWidget(mostrarCliente)
        self.diseño_lateral_derecho.addWidget(area_desplazamiento)
        
        # Insersión de los clientes en la tabla obtenidos de la base de datos
        clientes = self.db.consultar_Clientes()
        
        if clientes:
            mostrarCliente.setRowCount(len(clientes))
            for i, cliente in enumerate(clientes):
                for j, campo in enumerate(cliente):
                    item = QTableWidgetItem(str(campo))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(0, 0, 0))
                    mostrarCliente.setItem(i, j, item)
            mostrarCliente.itemClicked.connect(self.mostrar_cliente_seleccionado)
        else:
            mostrarCliente.setRowCount(1)
            mostrarCliente.setItem(0, 0, QTableWidgetItem("No hay clientes"))
            mostrarCliente.setColumnCount(1)
    
    def mostrar_cliente_seleccionado(self, item):
        row = item.row()
        idRenglon = item.tableWidget().item(row, 0).text()

        # Obtener información del cliente seleccionado
        cliente = self.db.consultar_Cliente_porId(idRenglon)
        mensaje = QMessageBox(self)
        mensaje.setWindowTitle("Información del cliente")
        mensaje.setText(f"Nombre: {cliente[1]}\nApellido Paterno: {cliente[2]}\nApellido Materno: {cliente[3]}\nTelefono: {cliente[4]}")
        cerrar = mensaje.addButton("Cerrar", QMessageBox.RejectRole)
        eliminar = mensaje.addButton("Eliminar", QMessageBox.AcceptRole)

        mensaje.exec_()

        if mensaje.clickedButton() == eliminar:
            self.db.eliminar_cliente(idRenglon)
            self.interfazClientes()
        
    def anadirCliente(self):
        # Ventana para añadir un cliente
        self.QDIalogCl = QDialog()
        nombre_cliente = QLineEdit()
        nombre_cliente.setPlaceholderText("Nombre del cliente")
        apellido_paterno = QLineEdit()
        apellido_paterno.setPlaceholderText("Apellido paterno")
        apellido_materno = QLineEdit()
        apellido_materno.setPlaceholderText("Apellido materno")
        telefono_cliente = QLineEdit()
        telefono_cliente.setPlaceholderText("Teléfono del cliente")
        self.layoutCl = QVBoxLayout()
        self.layoutCl.addWidget(nombre_cliente)
        self.layoutCl.addWidget(apellido_paterno)
        self.layoutCl.addWidget(apellido_materno)
        self.layoutCl.addWidget(telefono_cliente)
        boton = QPushButton("Añadir")

        boton.clicked.connect(lambda: self.insertarCliente(nombre_cliente.text(), apellido_paterno.text(), apellido_materno.text(), telefono_cliente.text()))
        self.layoutCl.addWidget(boton)
        self.QDIalogCl.setLayout(self.layoutCl)
        self.QDIalogCl.exec()

    def insertarCliente(self, nombre_cliente, apellido_paterno, apellido_materno, telefono_cliente):
        try:
            if self.db.insertar_Cliente(nombre_cliente, apellido_paterno, apellido_materno, telefono_cliente):
                QMessageBox.information(self, "Cliente añadido", "Cliente añadido")
                self.limpiar_diseño(self.layoutCl)
                self.limpiar_diseño(self.diseño_lateral_derecho)
                self.limpiar_diseño(self.interfazEventos())
                self.QDIalogCl.close()
                self.interfazClientes()
                return
            else:
                QMessageBox.warning(self, "Error", f"Error al insertar el cliente, revise los campos")
        except Exception:
            QMessageBox.warning(self, "Error", f"Error al insertar el cliente, revise los campos")
            return
         
    def interfazEventos(self):
        # Limpiar el diseño lateral derecho
        self.limpiar_diseño(self.diseño_lateral_derecho)
        
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
                    if campo == None:
                        campo = "N/A"
                    item = QTableWidgetItem(str(campo))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(0, 0, 0))
                    mostrarProovedor.setItem(i, j, item)
        else:
            mostrarProovedor.setRowCount(1)
            mostrarProovedor.setItem(0, 0, QTableWidgetItem("No hay eventos"))
            mostrarProovedor.setColumnCount(1)
    
    def interfazEmpleados(self):
        # Limpiar el diseño lateral derecho
        self.limpiar_diseño(self.diseño_lateral_derecho)

        # Añadir botones
        diseño_botones = QVBoxLayout()
        boton_añadir = QPushButton("Añadir")
        boton_añadir.clicked.connect(self.insertarEmpleado)
        boton_añadir.setStyleSheet("background-color: #FF7E67; color: white;")
        diseño_botones.addWidget(boton_añadir)
        self.diseño_lateral_derecho.addLayout(diseño_botones)

        
        # Añadir nuevo contenido para la interfaz de empleados
        mostrarEmpleado = QTableWidget()
        mostrarEmpleado.setColumnCount(7)
        mostrarEmpleado.verticalHeader().setVisible(False)
        mostrarEmpleado.setEditTriggers(QTableWidget.NoEditTriggers)
        mostrarEmpleado.setSelectionBehavior(QTableWidget.SelectRows)
        mostrarEmpleado.setHorizontalHeaderLabels(["No.", "Nombre(s)", "Apellido P.", "Apellido M.", "Dirección", "Telefono", "Puesto"])
        mostrarEmpleado.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

        area_desplazamiento = QScrollArea()
        area_desplazamiento.setWidgetResizable(True)
        area_desplazamiento.setWidget(mostrarEmpleado)
        self.diseño_lateral_derecho.addWidget(area_desplazamiento)
        
        # Insersión de los empleados en la tabla obtenidos de la base de datos
        empleados = self.db.consultar_empleados()
        
        if empleados:
            mostrarEmpleado.setRowCount(len(empleados))
            for i, empleado in enumerate(empleados):
                for j, campo in enumerate(empleado):
                    item = QTableWidgetItem(str(campo))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(0, 0, 0))
                    mostrarEmpleado.setItem(i, j, item)
            mostrarEmpleado.itemClicked.connect(self.mostrar_empleado_seleccionado)
        else:
            mostrarEmpleado.setRowCount(1)
            mostrarEmpleado.setItem(0, 0, QTableWidgetItem("No hay empleados"))
            mostrarEmpleado.setColumnCount(1)

    def mostrar_empleado_seleccionado(self, item):
        row = item.row()
        idRenglon = item.tableWidget().item(row, 0).text()

        # Obtener información del empleado seleccionado
        empleado = self.db.consultar_empleado(idRenglon)

        puesto = empleado[6]
        puesto = self.db.consultar_Puesto(puesto)
        puesto = puesto[0]

        mensaje = QMessageBox(self)
        mensaje.setWindowTitle("Información del empleado")
        mensaje.setText(f"No. {empleado[0]}\nNombre: {empleado[1]}\nApellido Paterno: {empleado[2]}\nApellido Materno: {empleado[3]}\nDirección: {empleado[4]}\nTelefono: {empleado[5]}\nPuesto: {puesto}")
        cerrar = mensaje.addButton("Cerrar", QMessageBox.RejectRole)

        if puesto != "Gerente":
            eliminar = mensaje.addButton("Eliminar", QMessageBox.AcceptRole)

        mensaje.exec_()

        if puesto != "Gerente":
            if mensaje.clickedButton() == eliminar:
                self.db.eliminar_empleado(idRenglon)
                self.interfazEmpleados()

    def insertarEmpleado(self):
        # Ventana para añadir un empleado
        self.QDIalogEm = QDialog()
        nombre_empleado = QLineEdit()
        nombre_empleado.setPlaceholderText("Nombre del empleado")
        apellido_paterno = QLineEdit()
        apellido_paterno.setPlaceholderText("Apellido paterno")
        apellido_materno = QLineEdit()
        apellido_materno.setPlaceholderText("Apellido materno")
        direccion_empleado = QLineEdit()
        direccion_empleado.setPlaceholderText("Dirección del empleado")
        telefono_empleado = QLineEdit()
        telefono_empleado.setPlaceholderText("Teléfono del empleado")
        puesto_empleado = QComboBox()

        # Campos para crear el usuario y contraseña del empleado
        usuario_empleado = QLineEdit()
        usuario_empleado.setPlaceholderText("Usuario del empleado")
        contraseña_empleado = QLineEdit()
        contraseña_empleado.setPlaceholderText("Contraseña del empleado")
        contraseña_empleado.setEchoMode(QLineEdit.Password)
        usuario_correo = QLineEdit()
        usuario_correo.setPlaceholderText("Correo del empleado")
        
        puestos = self.db.consultar_Puestos()

        for puesto in puestos:
            puesto_empleado.addItem(puesto[1])

        self.layoutEm = QVBoxLayout()
        self.layoutEm.addWidget(nombre_empleado)
        self.layoutEm.addWidget(apellido_paterno)
        self.layoutEm.addWidget(apellido_materno)
        self.layoutEm.addWidget(direccion_empleado)
        self.layoutEm.addWidget(telefono_empleado)
        self.layoutEm.addWidget(puesto_empleado)
        self.layoutEm.addWidget(usuario_empleado)
        self.layoutEm.addWidget(contraseña_empleado)
        self.layoutEm.addWidget(usuario_correo)

        boton = QPushButton("Añadir")
        boton.clicked.connect(lambda: self.IngresarEmpleado(nombre_empleado.text(), apellido_paterno.text(), apellido_materno.text(), direccion_empleado.text(), telefono_empleado.text(), puesto_empleado.currentIndex()+1, puesto_empleado.currentText(), usuario_empleado.text(), contraseña_empleado.text(), usuario_correo.text()))
        self.layoutEm.addWidget(boton)
        self.QDIalogEm.setLayout(self.layoutEm)
        self.QDIalogEm.exec()

    def IngresarEmpleado(self, nombre_empleado, apellido_paterno, apellido_materno, direccion_empleado, telefono_empleado, puesto_empleado, puesto_empleado_text, usuario_empleado, contraseña_empleado, usuario_correo):
        try:
            if self.db.insertar_Empleado(nombre_empleado, apellido_paterno, apellido_materno, direccion_empleado, telefono_empleado, puesto_empleado, puesto_empleado_text, usuario_empleado, contraseña_empleado, usuario_correo):
                QMessageBox.information(self, "Empleado añadido", "Empleado añadido")
                self.limpiar_diseño(self.layoutEm)
                self.limpiar_diseño(self.diseño_lateral_derecho)
                self.limpiar_diseño(self.interfazEmpleados())
                self.QDIalogEm.close()
                self.interfazEmpleados()
                self.interfazClientes()
                return
            else:
                QMessageBox.warning(self, "Error", f"Error al insertar el empleado, revise los campos")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al insertar el empleado. Error: {e}")
            return

    def limpiar_diseño(self, layout):
        try:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.limpiar_diseño(item.layout())
        except Exception as e:
            print(e)

    def interfazSalones(self):
        # Limpiar el diseño lateral derecho
        self.limpiar_diseño(self.diseño_lateral_derecho)

        # Añadir botones
        diseño_botones = QVBoxLayout()
        boton_añadir = QPushButton("Añadir")
        boton_añadir.clicked.connect(self.anadirSalon)
        boton_añadir.setStyleSheet("background-color: #FF7E67; color: white;")
        diseño_botones.addWidget(boton_añadir)
        self.diseño_lateral_derecho.addLayout(diseño_botones)


        # Añadir nuevo contenido para la interfaz de salones
        tablaSalones = QTableWidget()
        tablaSalones.setColumnCount(2)
        tablaSalones.verticalHeader().setVisible(False)
        tablaSalones.setEditTriggers(QTableWidget.NoEditTriggers)
        tablaSalones.setSelectionBehavior(QTableWidget.SelectRows)
        tablaSalones.setHorizontalHeaderLabels(["No.", "Salón"])
        tablaSalones.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

        area_desplazamiento = QScrollArea()
        area_desplazamiento.setWidgetResizable(True)
        area_desplazamiento.setWidget(tablaSalones)
        self.diseño_lateral_derecho.addWidget(area_desplazamiento)

        # Insersión de los salones en la tabla obtenidos de la base de datos
        salones = self.db.consultar_Salones()
        if salones:
            tablaSalones.setRowCount(len(salones))
            for i, salon in enumerate(salones):
                for j, campo in enumerate(salon):
                    item = QTableWidgetItem(str(campo))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(0, 0, 0))
                    tablaSalones.setItem(i, j, item)

    def anadirSalon(self):
        # Ventana para añadir un salon
        self.QDIalogSa = QDialog()
        nombre_salon = QLineEdit()
        nombre_salon.setPlaceholderText("Nombre del salon")

        self.layoutSa = QVBoxLayout()
        self.layoutSa.addWidget(nombre_salon)
        boton = QPushButton("Añadir")
        boton.clicked.connect(lambda: self.ingresarSalon(nombre_salon.text()))
        self.layoutSa.addWidget(boton)
        self.QDIalogSa.setLayout(self.layoutSa)
        self.QDIalogSa.exec()

    def ingresarSalon(self, nombre_salon):
        try:
            if self.db.insertar_Salon(nombre_salon):
                QMessageBox.information(self, "Salon añadido", "Salon añadido")
                self.limpiar_diseño(self.layoutSa)
                self.limpiar_diseño(self.diseño_lateral_derecho)
                self.limpiar_diseño(self.interfazSalones())
                self.QDIalogSa.close()
                self.interfazSalones()
                return
            else:
                QMessageBox.warning(self, "Error", f"Error al insertar el salon, revise los campos")
        except Exception:
            QMessageBox.warning(self, "Error", f"Error al insertar el salon, revise los campos")

    def ventanaPagos(self):
        # Limpiar el diseño lateral derecho
        self.limpiar_diseño(self.diseño_lateral_derecho)
        
        # Interfaz de pagos
        tablaPagos = QTableWidget()
        tablaPagos.setColumnCount(7)
        tablaPagos.setEditTriggers(QTableWidget.NoEditTriggers)
        tablaPagos.setSelectionBehavior(QTableWidget.SelectRows)
        tablaPagos.verticalHeader().setVisible(False)
        tablaPagos.setHorizontalHeaderLabels(["No.", "No. Evento", "P.I", "Fecha", "Fecha", "Estado", "Cliente"])
        tablaPagos.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
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
        else:
            tablaPagos.setRowCount(1)
            tablaPagos.setItem(0, 0, QTableWidgetItem("No hay pagos"))
            tablaPagos.setColumnCount(1)
    
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
            tabla_proveedores.setColumnCount(4)
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
            tabla_proveedores.itemClicked.connect(self.proveedorClicado)
            
            area_desplazamiento = QScrollArea()
            area_desplazamiento.setWidgetResizable(True)
            area_desplazamiento.setWidget(tabla_proveedores)
            self.diseño_lateral_derecho.addWidget(area_desplazamiento)
        else:
            etiqueta_proveedores.setText("No hay proveedores")
            self.diseño_lateral_derecho.addWidget(etiqueta_proveedores)

    def proveedorClicado(self, item):
        row = item.row()
        idRenglon = item.tableWidget().item(row, 0).text()
        
        # Obtener información del proveedor seleccionado
        mensaje = QMessageBox(self)
        mensaje.setWindowTitle("Información del proveedor")
        mensaje.setText(f"Proveedor: {item.tableWidget().item(row, 1).text()}")
        cerrar = mensaje.addButton("Cerrar", QMessageBox.RejectRole)
        eliminar = mensaje.addButton("Eliminar", QMessageBox.AcceptRole)

        mensaje.exec_()

        if mensaje.clickedButton() == eliminar:
            self.db.eliminar_proveedor(idRenglon)
            self.interfazProveedores()

    def eliminar_proveedor(self, id):
        self.db.eliminar_proveedor(id)
        self.interfazProveedores()

    def anadirProveedor(self):
        # Ventana para añadir un proveedor
        self.QDIalogPr = QDialog()
        nombre_proveedor = QLineEdit()
        nombre_proveedor.setPlaceholderText("Nombre del proveedor")
        correo_proveedor = QLineEdit()
        correo_proveedor.setPlaceholderText("Correo del proveedor")
        servicio_proveedor = QLineEdit()
        servicio_proveedor.setPlaceholderText("Servicio del proveedor")

        self.layoutPr = QVBoxLayout()
        self.layoutPr.addWidget(nombre_proveedor)
        self.layoutPr.addWidget(correo_proveedor)
        self.layoutPr.addWidget(servicio_proveedor)
        boton = QPushButton("Añadir")
        boton.clicked.connect(lambda: self.insertarProveedor(nombre_proveedor.text(), correo_proveedor.text(), servicio_proveedor.text()))
        self.layoutPr.addWidget(boton)
        self.QDIalogPr.setLayout(self.layoutPr)
        self.QDIalogPr.exec()

    def insertarProveedor(self, nombre_proveedor, correo_proveedor, servicio_proveedor):
        try:
            if self.db.insertar_Proveedor(nombre_proveedor, correo_proveedor, servicio_proveedor):
                QMessageBox.information(self, "Proveedor añadido", "Proveedor añadido")
                self.limpiar_diseño(self.layoutPr)
                self.limpiar_diseño(self.diseño_lateral_derecho)
                self.limpiar_diseño(self.interfazProveedores())
                self.QDIalogPr.close()
                self.interfazProveedores()
                return
            else:
                QMessageBox.warning(self, "Error", f"Error al insertar el proveedor, revise los campos")
        except Exception:
            QMessageBox.warning(self, "Error", f"Error al insertar el proveedor, revise los campos")
            return
        
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
            tabla_servicios.itemClicked.connect(self.servicioClicado)
            
            area_desplazamiento = QScrollArea()
            area_desplazamiento.setWidgetResizable(True)
            area_desplazamiento.setWidget(tabla_servicios)
            self.diseño_lateral_derecho.addWidget(area_desplazamiento)
        else:
            etiqueta_servicios_evento.setText("No hay servicios de eventos")
            self.diseño_lateral_derecho.addWidget(etiqueta_servicios_evento)

    def servicioClicado(self, item):
        row = item.row()
        idRenglon = item.tableWidget().item(row, 0).text()
        
        # Obtener información del servicio seleccionado
        mensaje = QMessageBox(self)
        mensaje.setWindowTitle("Información del servicio")
        mensaje.setText(f"Servicio: {item.tableWidget().item(row, 1).text()}")
        cerrar = mensaje.addButton("Cerrar", QMessageBox.RejectRole)
        eliminar = mensaje.addButton("Eliminar", QMessageBox.AcceptRole)

        mensaje.exec_()

        if mensaje.clickedButton() == eliminar:
            self.db.eliminar_servicio(idRenglon)
            self.interfazServiciosEvento()
    
    def anadirServicio(self):
        # Ventana para añadir un servicio
        self.QDIalogSe = QDialog()
        nombre_servicio = QLineEdit()
        nombre_servicio.setPlaceholderText("Nombre del servicio")
        descripcion_servicio = QLineEdit()
        descripcion_servicio.setPlaceholderText("Descripción del servicio")
        telefono_servicio = QLineEdit()
        telefono_servicio.setPlaceholderText("Teléfono del servicio")

        self.layoutEv = QVBoxLayout()
        self.layoutEv.addWidget(nombre_servicio)
        self.layoutEv.addWidget(descripcion_servicio)
        self.layoutEv.addWidget(telefono_servicio)
        boton = QPushButton("Añadir")
        boton.clicked.connect(lambda: self.ingresarServicio(nombre_servicio.text(), descripcion_servicio.text(), telefono_servicio.text()))
        self.layoutEv.addWidget(boton)
        self.QDIalogSe.setLayout(self.layoutEv)
        self.QDIalogSe.exec()

    def ingresarServicio(self, nombre_servicio, descripcion_servicio, telefono_servicio):
        try:
            if self.db.insertar_Servicio(nombre_servicio, descripcion_servicio, telefono_servicio):
                QMessageBox.information(self, "Servicio añadido", "Servicio añadido")
                self.limpiar_diseño(self.layoutEv)
                self.limpiar_diseño(self.diseño_lateral_derecho)
                self.limpiar_diseño(self.interfazServiciosEvento())
                self.QDIalogSe.close()
                self.interfazServiciosEvento()
                return
            else:
                QMessageBox.warning(self, "Error", f"Error al insertar el servicio, revise los campos")
        except Exception:
            QMessageBox.warning(self, "Error", f"Error al insertar el servicio, revise los campos")
            return
    
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
                for j, campo in enumerate(pago):
                    if campo == None:
                        campo = "N/A"
                    item = QTableWidgetItem(str(campo))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(0, 0, 0))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    tablaPagos.setItem(i, j, item)
            tablaPagos.itemClicked.connect(self.eventoClicado)
        tablaPagos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
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
        imprimirbt.clicked.connect(lambda: self.imprimir(evento))
        
        mensaje.exec_()
    
    def imprimir(self, evento):
        # Imprime un PDF con la información del evento seleccionado
        self.pdf = pdf()
        self.pdf.generar_evento(evento)

        
if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaAdmin()
    ventana.show()
    app.exec()