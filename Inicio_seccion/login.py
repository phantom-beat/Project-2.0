import sys
import requests
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from olvidaste_tu_contrasena import ForgotPasswordWindow  # Ajustar el import al nombre correcto

# Crear la aplicación
app = QApplication(sys.argv)

# Crear la ventana principal
window = QMainWindow()
window.setWindowTitle("NutriclinicIMB - Inicio de Sesión")
window.setGeometry(100, 100, 400, 500)

# Widget central y layout principal
central_widget = QWidget()
window.setCentralWidget(central_widget)
layout = QVBoxLayout(central_widget)

# Estilo general para el fondo blanco
central_widget.setStyleSheet("background-color: white;")

# Título principal
title = QLabel("Sistema de Gestión Nutricional")
title.setAlignment(Qt.AlignCenter)
title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 30px 0;")
layout.addWidget(title)

# Contenedor para los campos de entrada (para centrarlos)
form_container = QWidget()
form_layout = QVBoxLayout(form_container)

# Campo de Email
email_label = QLabel("E-mail")
email_label.setStyleSheet("font-size: 14px; margin-bottom: 5px; color: black; font-weight: bold;")
form_layout.addWidget(email_label)

email_input = QLineEdit()
email_input.setPlaceholderText("Ingresa tu email")
email_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; width: 300px; color: black; font-weight: normal;")
email_input.setFixedWidth(300)
form_layout.addWidget(email_input)

# Espaciado entre campos
form_layout.addSpacing(10)

# Campo de Contraseña
password_label = QLabel("Contraseña")
password_label.setStyleSheet("font-size: 14px; margin-bottom: 5px; color: black; font-weight: bold;")
form_layout.addWidget(password_label)

password_input = QLineEdit()
password_input.setPlaceholderText("Ingresa tu contraseña")
password_input.setEchoMode(QLineEdit.Password)
password_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; width: 300px; color: black; font-weight: normal;")
password_input.setFixedWidth(300)
form_layout.addWidget(password_input)

# Añadir el contenedor de los campos al layout principal, centrado
layout.addWidget(form_container, alignment=Qt.AlignCenter)

# Espaciado antes del botón
layout.addSpacing(20)

# Función para manejar el inicio de sesión
def login():
    email = email_input.text()
    password = password_input.text()

    try:
        response = requests.post("http://localhost:5000/login", json={"email": email, "password": password})
        if response.status_code == 200:
            QMessageBox.information(window, "Éxito", "Inicio de sesión exitoso")
        else:
            QMessageBox.warning(window, "Error", "Email o contraseña incorrectos")
    except requests.exceptions.RequestException as e:
        QMessageBox.critical(window, "Error", f"No se pudo conectar al servidor: {str(e)}")

# Botón de Log In
login_button = QPushButton("Log In")
login_button.setStyleSheet("""
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
login_button.clicked.connect(login)
layout.addWidget(login_button, alignment=Qt.AlignCenter)

# Espaciado después del botón
layout.addSpacing(10)

# Función para abrir la ventana de "Olvidaste tu contraseña"
def open_forgot_password():
    try:
        # Almacenar la ventana como un atributo de la ventana principal para mantener la referencia
        window.forgot_window = ForgotPasswordWindow()
        window.forgot_window.show()
    except Exception as e:
        QMessageBox.critical(window, "Error", f"No se pudo abrir la ventana de recuperación: {str(e)}")

# Enlace "¿Olvidaste tu contraseña?" como QPushButton
forgot_password = QPushButton("¿Olvidaste tu contraseña?")
forgot_password.setStyleSheet("""
    QPushButton {
        color: #007BFF;
        font-size: 12px;
        background: none;
        border: none;
        padding: 0;
        margin-bottom: 5px;
    }
    QPushButton:hover {
        text-decoration: underline;
    }
""")
forgot_password.setCursor(Qt.PointingHandCursor)
forgot_password.clicked.connect(open_forgot_password)  # Conectar el clic
layout.addWidget(forgot_password, alignment=Qt.AlignCenter)

# Enlace "¿No tienes cuenta? Regístrate" como QPushButton
register = QPushButton("¿No tienes cuenta? Regístrate")
register.setStyleSheet("""
    QPushButton {
        color: #007BFF;
        font-size: 12px;
        background: none;
        border: none;
        padding: 0;
        margin-bottom: 20px;
    }
    QPushButton:hover {
        text-decoration: underline;
    }
""")
register.setCursor(Qt.PointingHandCursor)
layout.addWidget(register, alignment=Qt.AlignCenter)

# Footer
footer = QLabel("NutriclinicIMB - 2025")
footer.setAlignment(Qt.AlignCenter)
footer.setStyleSheet("color: gray; font-size: 12px; margin-top: 30px;")
layout.addWidget(footer)

# Mostrar la ventana
window.show()

# Ejecutar la aplicación
sys.exit(app.exec())