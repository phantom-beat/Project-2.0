from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QMessageBox, QDateEdit,
    QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QDate, Signal

from Dashboard.Registrar_medidas.registrarmedidas import AnthropometryRegisterWindow
from database.db import SessionLocal
from models.paciente import Paciente

class RegistrarUsuarioWindow(QMainWindow):
    paciente_registrado = Signal(dict)

    def __init__(self, usuario_id):
        super().__init__()
        self.usuario_id = usuario_id
        self.setWindowTitle("Registrar Paciente")
        self.setGeometry(100, 100, 500, 700)

        outer_widget = QWidget()
        outer_layout = QVBoxLayout(outer_widget)
        outer_layout.setContentsMargins(40, 40, 40, 40)
        outer_layout.setSpacing(20)
        self.setCentralWidget(outer_widget)

        outer_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        form_container = QWidget()
        self.layout = QVBoxLayout(form_container)
        form_container.setStyleSheet("background-color: white; color: black; border-radius: 10px;")
        outer_layout.addWidget(form_container, alignment=Qt.AlignCenter)

        title = QLabel("Registro de pacientes")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px 0;")
        self.layout.addWidget(title)

        self.fields = {}

        def add_field(label_text, name, input_type="line", placeholder=""):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
            self.layout.addWidget(label)

            if input_type == "date":
                input_widget = QDateEdit()
                input_widget.setDate(QDate.currentDate())
                input_widget.setCalendarPopup(True)
            else:
                input_widget = QLineEdit()
                input_widget.setPlaceholderText(placeholder)

            input_widget.setFixedWidth(300)
            input_widget.setStyleSheet(
                "padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px;"
            )
            self.layout.addWidget(input_widget, alignment=Qt.AlignCenter)
            self.layout.addSpacing(10)
            self.fields[name] = input_widget

        add_field("Nombre paciente", name="nombre", placeholder="Ej: Juan Perez")
        add_field("Identificación del paciente", name="patient_id", placeholder="Número de documento")
        add_field("Fecha de Nacimiento", name="date", input_type="date")
        add_field("Sexo", name="sexo", placeholder="Masculino o femenino")
        add_field("Edad", name="edad", placeholder="Ej: 68")
        add_field("Teléfono", name="telefono", placeholder="Ej: 3001234567")
        add_field("Dirección", name="direccion", placeholder="Ej: Calle 123 #45-67")

        self.btn_registrar_paciente = QPushButton("Registrar paciente")
        self.btn_registrar_paciente.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.btn_registrar_paciente.clicked.connect(self.guardar_usuario)
        self.layout.addWidget(self.btn_registrar_paciente, alignment=Qt.AlignCenter)

        self.btn_registrar_medidas = QPushButton("Registrar medidas antropométricas")
        self.btn_registrar_medidas.setVisible(False)
        self.btn_registrar_medidas.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.btn_registrar_medidas.clicked.connect(self.abrir_ventana_medidas)
        self.layout.addWidget(self.btn_registrar_medidas, alignment=Qt.AlignCenter)

        self.btn_volver = QPushButton("Volver al inicio")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        self.btn_volver.clicked.connect(self.close)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        outer_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def guardar_usuario(self):
        nombre = self.fields["nombre"].text().strip()
        cedula = self.fields["patient_id"].text().strip()
        fecha_nacimiento = self.fields["date"].date().toPython()
        sexo = self.fields["sexo"].text().strip()
        edad = self.fields["edad"].text().strip()
        telefono = self.fields["telefono"].text().strip()
        direccion = self.fields["direccion"].text().strip()

        if not nombre or not cedula:
            QMessageBox.warning(self, "Campos incompletos", "Nombre y cédula son obligatorios.")
            return

        try:
            db = SessionLocal()
            existente = db.query(Paciente).filter_by(cedula=cedula).first()
            if existente:
                QMessageBox.information(self, "Paciente ya registrado", "Ya existe un paciente con esta cédula.")
                db.close()
                return

            nuevo = Paciente(
                nombre=nombre,
                cedula=cedula,
                fecha_nacimiento=fecha_nacimiento,
                sexo=sexo,
                edad=int(edad),
                telefono=telefono,
                direccion=direccion,
                usuario_id= self.usuario_id
            )
            db.add(nuevo)
            db.commit()

            QMessageBox.information(self, "Éxito", f"Paciente {nombre} registrado correctamente.")

            self.paciente_registrado.emit({
                "nombre": nombre,
                "cedula": cedula,
                "fecha_nac": fecha_nacimiento.strftime("%Y-%m-%d"),
                "edad": edad,
                "sexo": sexo
            })

            self.btn_registrar_medidas.setVisible(True)

        except Exception as e:
            db.rollback()
            QMessageBox.critical(self, "Error", f"Error al guardar en la base de datos:\n{e}")
        finally:
            db.close()

    def abrir_ventana_medidas(self):
        self.ventana_medidas = AnthropometryRegisterWindow()
        self.ventana_medidas.fields["patient_id"].setText(self.fields["patient_id"].text())
        self.ventana_medidas.show()


if __name__ == "__main__":
    app = QApplication([])
    window = RegistrarUsuarioWindow()
    window.show()
    app.exec()
