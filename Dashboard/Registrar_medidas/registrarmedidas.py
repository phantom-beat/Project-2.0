import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QDateEdit
)
from PySide6.QtCore import Qt, QDate
from datetime import datetime

from database.db import SessionLocal
from models.medicion import Medicion
from models.paciente import Paciente

class AnthropometryRegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Medidas Antropométricas")
        self.setGeometry(100, 100, 400, 600)
        self.fields = {}

        # Layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        central_widget.setStyleSheet("background-color: white;")

        # Título
        title = QLabel("Registro de Medidas Antropométricas")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 30px 0; color: black;")
        layout.addWidget(title)

        # Función para agregar campos
        def add_field(label_text, name, input_type="line", placeholder=""):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
            layout.addWidget(label)

            if input_type == "date":
                input_widget = QDateEdit()
                input_widget.setDate(QDate.currentDate())
                input_widget.setCalendarPopup(True)
            else:
                input_widget = QLineEdit()
                input_widget.setPlaceholderText(placeholder)

            input_widget.setFixedWidth(300)
            input_widget.setStyleSheet(
                "padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; color: black;"
            )
            layout.addWidget(input_widget, alignment=Qt.AlignCenter)
            layout.addSpacing(10)
            self.fields[name] = input_widget

        # Campos del formulario
        add_field("Fecha de evaluación", "date", input_type="date")
        add_field("Identificación del paciente", "patient_id", placeholder="Número de documento")
        add_field("Altura (cm)", "height", placeholder="Ej: 170")
        add_field("Peso (kg)", "weight", placeholder="Ej: 68.5")
        add_field("Circunferencia de cintura (cm)", "waist")
        add_field("Circunferencia de cadera (cm)", "hip")
        add_field("Pliegue tricipital (mm)", "triceps")
        add_field("Pliegue subescapular (mm)", "subscapular")

        # Botón de guardar
        submit_button = QPushButton("Guardar Medidas")
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
                width: 300px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        submit_button.clicked.connect(self.submit_data)
        layout.addWidget(submit_button, alignment=Qt.AlignCenter)

    def set_patient_id(self, cedula):
        """ Método seguro para establecer la cédula del paciente """
        self.fields["patient_id"].setText(cedula)
        self.fields["patient_id"].setReadOnly(True)

    def submit_data(self):
        try:
            data = {}
            for key, widget in self.fields.items():
                if isinstance(widget, QDateEdit):
                    data[key] = widget.date().toPython()
                else:
                    value = widget.text().strip()
                    if not value:
                        QMessageBox.warning(self, "Campo incompleto", f"Por favor completa el campo: {key}")
                        return
                    data[key] = value

            db = SessionLocal()
            paciente = db.query(Paciente).filter_by(cedula=data["patient_id"]).first()
            if not paciente:
                QMessageBox.warning(self, "Paciente no encontrado", "No existe un paciente con esta cédula.")
                return

            nueva_medicion = Medicion(
                date=data["date"],
                patient_id=data["patient_id"],
                height=float(data["height"]),
                weight=float(data["weight"]),
                waist=float(data["waist"]),
                hip=float(data["hip"]),
                triceps=float(data["triceps"]),
                subscapular=float(data["subscapular"])
            )

            db.add(nueva_medicion)
            db.commit()
            QMessageBox.information(self, "Éxito", "Medidas guardadas correctamente.")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar en la base de datos:\n{e}")
        finally:
            db.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnthropometryRegisterWindow()
    window.show()
    sys.exit(app.exec())
