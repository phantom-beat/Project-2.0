import sys
import os

# Añadir la raíz del proyecto al path para importar correctamente
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from database.db import SessionLocal
from models.usuario import Usuario
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
                               QLineEdit, QComboBox, QCheckBox, QPushButton, QMessageBox)
from PySide6.QtCore import Qt

class RegisterWindow(QMainWindow):
    def __init__(self, login_window=None):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("NutriClinicIMB - Registro")
        self.setGeometry(100, 100, 400, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        central_widget.setStyleSheet("background-color: white;")

        title = QLabel("Registro de Nuevo Usuario")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 30px 0;")
        layout.addWidget(title)

        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)

        # Nombre completo
        name_label = QLabel("Nombre completo")
        name_label.setStyleSheet("font-size: 14px; margin-bottom: 5px; font-weight: bold;")
        form_layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ingresa tu nombre completo")
        self.name_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px;")
        form_layout.addWidget(self.name_input)

        form_layout.addSpacing(10)

        # Número de identificación
        id_label = QLabel("Número de identificación")
        id_label.setStyleSheet(name_label.styleSheet())
        form_layout.addWidget(id_label)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Ingresa tu número de identificación")
        self.id_input.setStyleSheet(self.name_input.styleSheet())
        form_layout.addWidget(self.id_input)

        form_layout.addSpacing(10)

        # Rol
        role_label = QLabel("Seleccione su Rol")
        role_label.setStyleSheet(name_label.styleSheet())
        form_layout.addWidget(role_label)

        self.role_input = QComboBox()
        self.role_input.addItems(["Doctor/a", "Nutricionista", "Administrador/a", "Paciente"])
        self.role_input.setStyleSheet(self.name_input.styleSheet())
        form_layout.addWidget(self.role_input)

        form_layout.addSpacing(10)

        # Email
        email_label = QLabel("E-mail")
        email_label.setStyleSheet(name_label.styleSheet())
        form_layout.addWidget(email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ingresa tu email")
        self.email_input.setStyleSheet(self.name_input.styleSheet())
        form_layout.addWidget(self.email_input)

        form_layout.addSpacing(10)

        # Contraseña
        password_label = QLabel("Contraseña")
        password_label.setStyleSheet(name_label.styleSheet())
        form_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingresa tu contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.name_input.styleSheet())
        form_layout.addWidget(self.password_input)

        form_layout.addSpacing(10)

        # Confirmar contraseña
        confirm_password_label = QLabel("Confirmar contraseña")
        confirm_password_label.setStyleSheet(name_label.styleSheet())
        form_layout.addWidget(confirm_password_label)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirma tu contraseña")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(self.name_input.styleSheet())
        form_layout.addWidget(self.confirm_password_input)

        layout.addWidget(form_container, alignment=Qt.AlignCenter)
        layout.addSpacing(20)

        # Checkbox de términos
        self.terms_checkbox = QCheckBox("Acepto los términos y políticas de privacidad")
        self.terms_checkbox.setStyleSheet("font-size: 12px;")
        layout.addWidget(self.terms_checkbox, alignment=Qt.AlignCenter)

        layout.addSpacing(10)

        # Botón de registro
        register_button = QPushButton("Completar Registro...")
        register_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
                width: 300px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        register_button.clicked.connect(self.complete_registration)
        layout.addWidget(register_button, alignment=Qt.AlignCenter)

        layout.addSpacing(10)

        # Enlace para volver al login
        back_to_login = QPushButton("¿Ya tienes cuenta? Inicia sesión")
        back_to_login.setStyleSheet("""
            QPushButton {
                color: #007BFF;
                font-size: 12px;
                background: none;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        back_to_login.setCursor(Qt.PointingHandCursor)
        back_to_login.clicked.connect(self.back_to_login)
        layout.addWidget(back_to_login, alignment=Qt.AlignCenter)

        footer = QLabel("NutriClinicIMB - 2025")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: gray; font-size: 12px; margin-top: 30px;")
        layout.addWidget(footer)

    def complete_registration(self):
        name = self.name_input.text()
        identification = self.id_input.text()
        role = self.role_input.currentText()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        terms_accepted = self.terms_checkbox.isChecked()

        if not all([name, identification, role, email, password, confirm_password]):
            QMessageBox.warning(self, "Error", "Por favor, completa todos los campos")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            return

        if not terms_accepted:
            QMessageBox.warning(self, "Error", "Debes aceptar los términos y políticas de privacidad")
            return

        exito, mensaje = registrar_usuario(name, identification, role, email, password)
        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.close()
            if self.login_window:
                self.login_window.show()
        else:
            QMessageBox.warning(self, "Error", mensaje)

    def back_to_login(self):
        self.close()
        if self.login_window:
            self.login_window.show()

# --- FUNCIÓN que guarda el usuario en la base de datos ---
def registrar_usuario(name, identification, role, email, password):
    db = SessionLocal()
    try:
        usuario_existente = db.query(Usuario).filter_by(email=email).first()
        if usuario_existente:
            return False, "El correo ya está registrado."

        nuevo_usuario = Usuario(
            name=name,
            identification=identification,
            role=role,
            email=email
        )
        nuevo_usuario.set_password(password)

        db.add(nuevo_usuario)
        db.commit()
        return True, "Usuario registrado exitosamente."
    except Exception as e:
        db.rollback()
        return False, f"Error al registrar usuario: {str(e)}"
    finally:
        db.close()

# --- Ejecutar ventana si se corre directamente ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec())
