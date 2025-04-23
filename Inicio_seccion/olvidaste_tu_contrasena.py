import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt

class ForgotPasswordWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NutriclinicIMB - Olvidaste tu Contraseña")
        self.setGeometry(100, 100, 400, 400)

        # Widget central y layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Estilo general para el fondo blanco
        self.central_widget.setStyleSheet("background-color: white;")

        # Título
        self.title = QLabel("Recuperar Contraseña")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px 0;")
        self.layout.addWidget(self.title)

        # Contenedor para el formulario de email
        self.email_container = QWidget()
        self.email_layout = QVBoxLayout(self.email_container)

        # Campo de Email
        self.email_label = QLabel("E-mail")
        self.email_label.setStyleSheet("font-size: 14px; margin-bottom: 5px; color: black; font-weight: bold;")
        self.email_layout.addWidget(self.email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ingresa tu email")
        self.email_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; width: 300px; color: black; font-weight: normal;")
        self.email_input.setFixedWidth(300)
        self.email_layout.addWidget(self.email_input, alignment=Qt.AlignCenter)

        # Espaciado
        self.email_layout.addSpacing(20)

        # Botón de Enviar
        self.send_button = QPushButton("Enviar")
        self.send_button.setStyleSheet("""
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
        self.send_button.clicked.connect(self.verify_email)
        self.email_layout.addWidget(self.send_button, alignment=Qt.AlignCenter)

        # Añadir el contenedor de email al layout principal
        self.layout.addWidget(self.email_container, alignment=Qt.AlignCenter)

        # Contenedor para los campos de nueva contraseña (inicialmente oculto)
        self.password_container = QWidget()
        self.password_layout = QVBoxLayout(self.password_container)

        # Campo de Contraseña Nueva
        self.new_password_label = QLabel("Contraseña Nueva")
        self.new_password_label.setStyleSheet("font-size: 14px; margin-bottom: 5px; color: black; font-weight: bold;")
        self.password_layout.addWidget(self.new_password_label)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Ingresa tu nueva contraseña")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; width: 300px; color: black; font-weight: normal;")
        self.new_password_input.setFixedWidth(300)
        self.password_layout.addWidget(self.new_password_input, alignment=Qt.AlignCenter)

        # Espaciado
        self.password_layout.addSpacing(10)

        # Campo de Confirmar Contraseña
        self.confirm_password_label = QLabel("Confirmar Contraseña")
        self.confirm_password_label.setStyleSheet("font-size: 14px; margin-bottom: 5px; color: black; font-weight: bold;")
        self.password_layout.addWidget(self.confirm_password_label)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirma tu nueva contraseña")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; width: 300px; color: black; font-weight: normal;")
        self.confirm_password_input.setFixedWidth(300)
        self.password_layout.addWidget(self.confirm_password_input, alignment=Qt.AlignCenter)

        # Espaciado
        self.password_layout.addSpacing(20)

        # Botón de Guardar Contraseña
        self.save_button = QPushButton("Guardar Contraseña")
        self.save_button.setStyleSheet("""
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
        self.save_button.clicked.connect(self.save_new_password)
        self.password_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)

        # Añadir el contenedor de contraseña al layout principal, pero oculto inicialmente
        self.layout.addWidget(self.password_container, alignment=Qt.AlignCenter)
        self.password_container.hide()

    def verify_email(self):
        email = self.email_input.text()
        if email:
            # Simular verificación (en un sistema real, esto se conectaría al backend)
            QMessageBox.information(self, "Éxito", "Correo verificado correctamente")
            # Ocultar el formulario de email
            self.email_container.hide()
            # Mostrar el formulario de nueva contraseña
            self.password_container.show()
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingresa un email válido")

    def save_new_password(self):
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not new_password or not confirm_password:
            QMessageBox.warning(self, "Error", "Por favor, completa ambos campos")
        elif new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
        else:
            # Simular guardar la nueva contraseña (en un sistema real, esto se conectaría al backend)
            QMessageBox.information(self, "Éxito", "Contraseña actualizada correctamente")
            self.close()  # Cerrar la ventana después de guardar

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ForgotPasswordWindow()
    window.show()
    sys.exit(app.exec())