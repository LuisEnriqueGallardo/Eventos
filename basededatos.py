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
        
    def consultar_eventos(self):
        try:
            cons = "SELECT eventos.id_evento, eventos.fecha, clientes.nombres, clientes.telefono, salones.salon FROM eventos INNER JOIN clientes ON clientes.id_cliente = eventos.id_cliente INNER JOIN salones ON salones.id_salon = eventos.id_salon;"
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
        
    def consultar_Salones(self):
        try:
            cons = "SELECT * FROM salones"
            self.cursor.execute(cons)
            result = self.cursor.fetchall()
            return result
        except DatabaseError as e:
            print(f"Error al consultar salones: {e}")
            return None