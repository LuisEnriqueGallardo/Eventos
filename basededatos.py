import mysql.connector as driver
from mysql.connector import DatabaseError, IntegrityError
from datetime import date

class BaseDeDatos:
    def __init__(self):
        try:
            self.connection = driver.connect(
                host="localhost",
                user="invitado",
                password="invitado_password",
                database="eventos"
            )
            self.cursor = self.connection.cursor()
            print(f"Conexión exitosa a la base de datos 'eventos' como invitado")
        except DatabaseError as e:
            print(f"Error al conectar a la base de datos: {e}")
            
    def reconectar(self, usuario, contrasenia):
        try:
            self.connection = driver.connect(
                host="localhost",
                user=usuario,
                password=contrasenia,
                database="eventos"
            )
            self.cursor = self.connection.cursor()
            print(f"Conexión exitosa a la base de datos 'eventos' como {usuario}")
        except DatabaseError as e:
            print(f"Error al conectar a la base de datos: {e}")

    def autenticar_usuario(self, nombre_usuario, contrasenia):
        try:
            cons = "SELECT id_usuario, rol FROM usuario WHERE usuario = %s AND contrasenia = %s"
            self.cursor.execute(cons, (nombre_usuario, contrasenia))
            result = self.cursor.fetchone()
            if result:
                print(f"Usuario autenticado: {nombre_usuario}")
                return result[0], result[1]
            else:
                return False, False
        except DatabaseError as e:
            print(f"Error al autenticar usuario: {e}")
            return None
        
    def consultar_empleados(self):
        try:
            cons = "SELECT id_empleados_info, nombres, apellido_paterno, apellido_materno, direccion, telefono, puesto FROM empleados_info;"
            self.cursor.execute(cons)
            result = self.cursor.fetchall()
            return result
        except DatabaseError as e:
            print(f"Error al consultar empleados: {e}")
            return None

    def consultar_empleado(self, id_empleado):
        try:
            cons = "SELECT * FROM empleados_info where id_empleados_info = %s"
            params = (id_empleado,)
            self.cursor.execute(cons, params)
            result = self.cursor.fetchone()
            return result
        except DatabaseError as e:
            print(f"Error al consultar empleados: {e}")
            return None
        
    def consultar_Puesto(self, id_puesto):
        try:
            cons = "SELECT puesto FROM empleados WHERE id_empleado = %s"
            self.cursor.execute(cons, (id_puesto,))
            result = self.cursor.fetchone()
            return result
        except DatabaseError as e:
            print(f"Error al consultar puesto: {e}")
            return None
        
    def insertar_Empleado(self, nombres, apellido_paterno, apellido_materno, direccion, telefono, puesto, puestotext, usuario, contrasenia, correo):
        try:
            # Insertar empleado en empleados_info
            ins = "INSERT INTO empleados_info (nombres, apellido_paterno, apellido_materno, direccion, telefono, puesto) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(ins, (nombres, apellido_paterno, apellido_materno, direccion, telefono, puesto))
            self.connection.commit()

            # Obtener el id del empleado recién insertado
            id_empleado = self.cursor.lastrowid

            # Insertar usuario en la tabla usuario
            ins = "INSERT INTO usuario (usuario, correo, contrasenia, id_empleado, rol) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(ins, (usuario, correo, contrasenia, id_empleado, puestotext))
            self.connection.commit()

            return True
        except Exception as e:
            print("Error al insertar empleado:", e)
            return False

        
    def eliminar_empleado(self, id_empleado):
        try:
            # Eliminar las filas dependientes en la tabla usuario
            cons = "DELETE FROM usuario WHERE id_empleado = %s"
            self.cursor.execute(cons, (id_empleado,))
            self.connection.commit()

            # Eliminar la fila en la tabla empleados_info
            cons = "DELETE FROM empleados_info WHERE id_empleados_info = %s"
            self.cursor.execute(cons, (id_empleado,))
            self.connection.commit()

            return True
        except DatabaseError as e:
            print(f"Error al eliminar empleado: {e}")
            return False
    
    def consultar_Puestos(self):
        try:
            cons = "SELECT * FROM empleados"
            self.cursor.execute(cons)
            result = self.cursor.fetchall()
            return result
        except DatabaseError as e:
            print(f"Error al consultar puestos: {e}")
            return None
        
    def consultar_eventos(self):
        try:
            cons = "SELECT eventos.id_evento, eventos.fecha, clientes.nombres, clientes.telefono, salones.salon, eventos.descripcion FROM eventos INNER JOIN clientes ON clientes.id_cliente = eventos.id_cliente INNER JOIN salones ON salones.id_salon = eventos.id_salon;"
            self.cursor.execute(cons)
            result = self.cursor.fetchall()
            return result
        except DatabaseError as e:
            print(f"Error al consultar eventos: {e}")
            return None
        
    def consultar_evento_detallado(self, id_evento):
        try:
            cons = "SELECT eventos.id_evento, eventos.fecha, clientes.nombres, clientes.apellido_paterno, clientes.apellido_materno, clientes.telefono, salones.salon, eventos.descripcion FROM eventos INNER JOIN clientes ON clientes.id_cliente = eventos.id_cliente INNER JOIN salones ON salones.id_salon = eventos.id_salon WHERE eventos.id_evento = %s;"
            self.cursor.execute(cons, (id_evento,))
            result = self.cursor.fetchone()
            return result
        except DatabaseError as e:
            print(f"Error al consultar evento detallado: {e}")
            return None
    
    def insertar_evento(self, pagoinicial, monto, fecha, descripcion, clienteid, salon):
        try:
            salonid = "SELECT id_salon FROM salones WHERE salon = %s"
            self.cursor.execute(salonid, (salon,))
            salon = self.cursor.fetchone()[0]

            ins = "INSERT INTO eventos (fecha, descripcion, id_cliente, id_salon) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(ins, (fecha, descripcion, clienteid, salon))
            self.connection.commit()

            # Inserción de pago inicial
            self.insertar_Pago(self.cursor.lastrowid, monto, date.today(), pagoinicial)

            return True
        except DatabaseError as e:
            print(f"Error al insertar evento: {e}")
            return False
    
    def consultar_eventos_no_pagados(self):
        try:
            cons = "SELECT e.id_evento, e.fecha, e.descripcion, CONCAT(c.nombres, ' ', c.apellido_paterno, ' ', c.apellido_materno) AS nombre_completo, COALESCE(SUM(p.monto), 0) AS total, COALESCE(SUM(p.pago_inicial), 0) AS anticipo FROM eventos e INNER JOIN clientes c ON e.id_cliente = c.id_cliente LEFT JOIN pagos p ON e.id_evento = p.id_evento WHERE NOT EXISTS (SELECT 1 FROM pagos p2 WHERE p2.id_evento = e.id_evento AND p2.fecha_pago_final IS NOT NULL) GROUP BY e.id_evento, e.fecha, e.descripcion, c.nombres, c.apellido_paterno, c.apellido_materno;"
            self.cursor.execute(cons)
            result = self.cursor.fetchall()
            return result
        except DatabaseError as e:
            print(f"Error al consultar eventos no pagados: {e}")
            return None
    
    def consultar_eventos_pagados(self):
        try:
            cons = "SELECT e.id_evento, e.fecha, e.descripcion, CONCAT(c.nombres, ' ', c.apellido_paterno, ' ', c.apellido_materno) AS nombre_completo, SUM(p.monto) AS monto_total_pagado, MAX(p.fecha_pago_inicial) AS fecha_ultimo_pago FROM eventos e INNER JOIN clientes c ON e.id_cliente = c.id_cliente INNER JOIN pagos p ON e.id_evento = p.id_evento WHERE p.fecha_pago_final IS NOT NULL GROUP BY e.id_evento, e.fecha, e.descripcion, c.nombres, c.apellido_paterno, c.apellido_materno HAVING SUM(p.monto) >= (SELECT SUM(monto) FROM pagos WHERE id_evento = e.id_evento AND fecha_pago_final IS NOT NULL);"
            self.cursor.execute(cons)
            result = self.cursor.fetchall()
            return result
        except DatabaseError as e:
            print(f"Error al consultar eventos pagados: {e}")
            return None
        
    def consultar_Salones(self):
        try:
            cons = "SELECT * FROM salones"
            self.cursor.execute(cons)
            result = self.cursor.fetchall()
            return result
        except DatabaseError as e:
            print(f"Error al consultar salones: {e}")
            return None
        
    def insertar_Salon(self, nombre):
        try:
            ins = "INSERT INTO salones (salon) VALUES (%s)"
            self.cursor.execute(ins, (nombre,))
            self.connection.commit()
            return True
        except IntegrityError as e:
            print(f"Error al insertar salon: {e}")
            return False
        
    def consultar_Pagos(self):
        try:
            cons = "SELECT * FROM pagos"
            self.cursor.execute(cons)
            result = self.cursor.fetchall()
            pagos_detallados = []
            for idpago, idevento, monto, fechapagoinicial, pagoinicial, fechafinal in result:
                if fechafinal:
                    estado = 'PAGADO'
                else:
                    estado = 'INPAGO'
                pago_detallado = (idpago, idevento, monto, fechapagoinicial, pagoinicial, estado)
                pagos_detallados.append(pago_detallado)
            result = pagos_detallados
            return result
        except DatabaseError as e:
            print(f"Error al consultar pagos: {e}")
            return None
    
    def consultar_Pago(self, id_pago):
        try:
            cons = "SELECT * FROM pagos WHERE id_pago = %s"
            self.cursor.execute(cons, (id_pago,))
            result = self.cursor.fetchone()
            return result
        except DatabaseError as e:
            print(f"Error al consultar pago: {e}")
            return None
        
    def consultar_Cliente_porEvento(self, id_evento):
        try:
            cons = "SELECT clientes.nombres, clientes.apellido_paterno, clientes.apellido_materno FROM eventos INNER JOIN clientes ON clientes.id_cliente = eventos.id_cliente WHERE eventos.id_evento = %s"
            self.cursor.execute(cons, (id_evento,))
            result = self.cursor.fetchone()
            return result
        except DatabaseError as e:
            print(f"Error al consultar cliente por evento: {e}")
            return None
        
    def finalizar_Pago(self, id_pago):
        try:
            cons = "UPDATE pagos SET fecha_pago_final = %s WHERE id_pago = %s"
            self.cursor.execute(cons, (date.today(), id_pago))
            self.connection.commit()
            return True
        except DatabaseError as e:
            print(f"Error al finalizar pago: {e}")
            return False
    
    def consultar_Clientes(self):
        try:
            cons = "SELECT * FROM clientes"
            self.cursor.execute(cons)
            result = self.cursor.fetchall()
            return result
        except DatabaseError as e:
            print(f"Error al consultar clientes: {e}")
            return None
    
    def consultar_Cliente_porId(self, id_cliente):
        try:
            cons = "SELECT * FROM clientes WHERE id_cliente = %s"
            self.cursor.execute(cons, (id_cliente,))
            result = self.cursor.fetchone()
            return result
        except DatabaseError as e:
            print(f"Error al consultar cliente: {e}")
            return None
        
    def eliminar_cliente(self, id_cliente):
        try:
            cons = "DELETE FROM clientes WHERE id_cliente = %s"
            self.cursor.execute(cons, (id_cliente,))
            self.connection.commit()
            return True
        except DatabaseError as e:
            print(f"Error al eliminar cliente: {e}")
            return False
    
    def insertar_Cliente(self, nombres, apellido_paterno, apellido_materno, telefono):
        try:
            ins = "INSERT INTO clientes (nombres, apellido_paterno, apellido_materno, telefono) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(ins, (nombres, apellido_paterno, apellido_materno, telefono))
            self.connection.commit()
            return True
        except IntegrityError as e:
            print(f"Error al insertar cliente: {e}")
            return False
        
    def insertar_Pago(self, evento, monto, fechapagoinicial, pagoinicial):
        try:
            ins = "INSERT INTO pagos (id_evento, monto, fecha_pago_inicial, pago_inicial) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(ins, (evento, monto, fechapagoinicial, pagoinicial))
            self.connection.commit()
            return True
        except DatabaseError as e:
            print(f"Error al insertar pago: {e}")
            return False
    
    def consultar_Proveedores(self):
        try:
            cons = "SELECT * FROM proveedores"
            self.cursor.execute(cons)
            result = self.cursor.fetchall()
            return result
        except DatabaseError as e:
            print(f"Error al consultar proveedores: {e}")
            return None
        
    def eliminar_proveedor(self, id_proveedor):
        try:
            cons = "DELETE FROM proveedores WHERE id_proveedores = %s"
            self.cursor.execute(cons, (id_proveedor,))
            self.connection.commit()
            return True
        except DatabaseError as e:
            print(f"Error al eliminar proveedor: {e}")
            return False
    
    def insertar_Proveedor(self, nombre, correo, telefono):
        try:
            ins = "INSERT INTO proveedores (empresa, correo, servicio) VALUES (%s, %s, %s)"
            self.cursor.execute(ins, (nombre, correo, telefono))
            self.connection.commit()
            return True
        except IntegrityError as e:
            print(f"Error al insertar proveedor: {e}")
            return False
    
    def consultar_servicios(self):
        try:
            cons = "SELECT * FROM servicios_eventos"
            self.cursor.execute(cons)
            result = self.cursor.fetchall()
            return result
        except DatabaseError as e:
            print(f"Error al consultar servicios: {e}")
            return None

    def insertar_Servicio(self, nombre, descripcion, telefono):
        try:
            ins = "INSERT INTO servicios_eventos (servicio, descripcion, telefono) VALUES (%s, %s, %s)"
            self.cursor.execute(ins, (nombre, descripcion, telefono))
            self.connection.commit()
            return True
        except IntegrityError as e:
            print(f"Error al insertar servicio: {e}")
            return False