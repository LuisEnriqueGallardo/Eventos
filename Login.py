import sys
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QStatusBar, QMainWindow , QWidget
from administrador import VentanaAdmin
from basededatos import BaseDeDatos as bd
from recepcion import Recepcion
from organizador import VentanaPrincipal


class LoginWindow(QMainWindow):
    """Ventana de inicio de sesión

    Args:
        QWidget (QWidgetr): Ventana principal de la aplicación
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.resize(300, 150)
        widget = QWidget()
        
        # Etiqutas
        self.usuariolb = QLabel("USUARIO:")
        self.pdwlb = QLabel("CLAVE:")

        # Campos de texto
        self.usuario_in = QLineEdit()
        self.pwd_in = QLineEdit()
        self.pwd_in.setEchoMode(QLineEdit.Password)

        # Botón de login
        self.login_boton = QPushButton("INGRESAR")
        self.login_boton.setStyleSheet("background-color: #FF7E67; color: white;")
        self.login_boton.clicked.connect(self.login)
        self.login_boton.clicked.connect(self.login)
        
        self.usuario_in.returnPressed.connect(self.login)
        self.pwd_in.returnPressed.connect(self.login)
        
        # Barra de estado para el login erroneo
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("background-color: #ffdbd5;")

        # Diseño de la ventana
        layout_entrada = QVBoxLayout()
        layout_entrada.addWidget(self.usuariolb)
        layout_entrada.addWidget(self.usuario_in)
        layout_entrada.addWidget(self.pdwlb)
        layout_entrada.addWidget(self.pwd_in)

        layout_botones = QHBoxLayout()
        layout_botones.addStretch(1)
        layout_botones.addWidget(self.login_boton)
        layout_botones.addStretch(1)

        layout_principal = QVBoxLayout(widget)
        layout_principal.addLayout(layout_entrada)
        layout_principal.addLayout(layout_botones)

        layout_principal.addWidget(self.status_bar)
        
        self.setCentralWidget(widget)
        
    def login(self):
        """Funcion para autenticar al usuario en la base de datos
        """
        user = self.usuario_in.text()
        password = self.pwd_in.text()
        
        # Autenticar usuario en la base de datos y obtener el rol del usuario
        try:
            db = bd()
            id, rol = db.autenticar_usuario(user, password)
            if id and rol:
                if rol == "recepcion":
                    db.reconectar("recepcion", "recepcionpwd")
                    nombre = db.consultar_empleado(id)
                    self.window = Recepcion(nombre, db)
                elif rol == "organizador":
                    db.reconectar("organizador", "organizadorpwd")
                    nombre = db.consultar_empleado(id)
                    self.window = VentanaPrincipal(nombre, db)
                elif rol == "admin":
                    db.reconectar("administrador", "administradorpwd")
                    nombre = db.consultar_empleado(id)
                    self.window = VentanaAdmin(nombre, db)
                else:
                    return
                print(f"Usuario autenticado con rol {rol}")
                self.window.show()
                self.hide()
            else:
                print("Usuario o contraseña incorrectos")
                self.status_bar.showMessage("Usuario o contraseña incorrectos")
                
        except Exception as e:
            print("Error al conectar a la base de datos", e)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
    
