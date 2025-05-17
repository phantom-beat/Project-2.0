import os
import sys

# Añadir el directorio raíz del proyecto al path para permitir imports correctos
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette

from olvidaste_tu_contrasena import ForgotPasswordWindow
from Registro.Registro import RegisterWindow
from models.usuario import Usuario
from database.db import SessionLocal
from Dashboard.dashboard import DashboardWindow  

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("NutriclinicIMB - Inicio de Sesión")
        self.setGeometry(100, 100, 400, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        central_widget.setStyleSheet("background-color: white; color: black;")

        title = QLabel("Sistema de Gestión Nutricional")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 30px 0; color: black;")
        layout.addWidget(title)

        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(40, 10, 40, 10)

        # Campo Email
        email_label = QLabel("E-mail")
        email_label.setStyleSheet("font-size: 14px; margin-bottom: 5px; color: black; font-weight: bold;")
        form_layout.addWidget(email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ingresa tu email")
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 4px;
                color: black;
            }
            QLineEdit::placeholder {
                color: #aaa;
            }
        """)
        form_layout.addWidget(self.email_input)

        form_layout.addSpacing(15)

        # Campo Contraseña
        password_label = QLabel("Contraseña")
        password_label.setStyleSheet(email_label.styleSheet())
        form_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingresa tu contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.email_input.styleSheet())
        form_layout.addWidget(self.password_input)

        layout.addWidget(form_container)

        # Botón de Login
        login_button = QPushButton("Iniciar Sesión")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                padding: 12px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                margin: 20px 40px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        # Enlace "¿Olvidaste tu contraseña?"
        forgot_password = QPushButton("¿Olvidaste tu contraseña?")
        forgot_password.setStyleSheet("""
            QPushButton {
                color: #007BFF;
                font-size: 13px;
                background: none;
                border: none;
                padding: 5px;
                margin: 5px 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        forgot_password.setCursor(Qt.PointingHandCursor)
        forgot_password.clicked.connect(self.open_forgot_password)
        layout.addWidget(forgot_password, alignment=Qt.AlignCenter)

        # Enlace de Registro
        register = QPushButton("¿No tienes cuenta? Regístrate")
        register.setStyleSheet("""
            QPushButton {
                color: #007BFF;
                font-size: 13px;
                background: none;
                border: none;
                padding: 5px;
                margin: 5px 0 15px 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        register.setCursor(Qt.PointingHandCursor)
        register.clicked.connect(self.open_register)
        layout.addWidget(register, alignment=Qt.AlignCenter)

        # Footer
        footer = QLabel("NutriclinicIMB - 2025")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: gray; font-size: 12px; margin-top: 20px;")
        layout.addWidget(footer)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if email.strip() and password.strip():
            exito, mensaje, usuario = autenticar_usuario(email, password)
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                # Pasar el nombre del usuario al Dashboard
                self.dashboard = DashboardWindow(user_id=usuario.id, user_name=usuario.name)
                self.dashboard.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", mensaje)
        else:
            QMessageBox.warning(self, "Error", "Por favor ingrese email y contraseña")

    def open_forgot_password(self):
        try:
            self.forgot_window = ForgotPasswordWindow()
            self.forgot_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir la ventana: {str(e)}")

    def open_register(self):
        try:
            self.register_window = RegisterWindow()
            self.register_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir la ventana de registro: {str(e)}")


# Función para validar usuario
def autenticar_usuario(email, password):
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(Usuario.email == email).first()
        if usuario and usuario.check_password(password):
            return True, "Inicio de sesión exitoso", usuario
        else:
            return False, "Email o contraseña incorrectos", None
    except Exception as e:
        return False, f"Error al autenticar: {str(e)}", None
    finally:
        db.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = app.palette()
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
    app.setPalette(palette)

    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
