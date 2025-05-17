from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QDateEdit, QComboBox
)
from PySide6.QtCore import Qt, QDate
from database.db import SessionLocal
from models.paciente_neonato import PacienteNeonato


class RegistrarNeonatoWindow(QMainWindow):
    def __init__(self,usuario_id):
        super().__init__()
        self.usuario_id = usuario_id
        self.setWindowTitle("Registro de Neonato")
        self.setGeometry(200, 200, 400, 500)

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        self.fields = {}

        def add_field(label_text, key, input_type="line"):
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold;")
            layout.addWidget(label)

            if input_type == "date":
                input_widget = QDateEdit()
                input_widget.setDate(QDate.currentDate())
                input_widget.setCalendarPopup(True)
            elif input_type == "combo":
                input_widget = QComboBox()
                input_widget.addItems(["Masculino", "Femenino"])
            else:
                input_widget = QLineEdit()

            input_widget.setStyleSheet("padding: 6px;")
            layout.addWidget(input_widget)
            self.fields[key] = input_widget

        add_field("Nombre", "nombre")
        add_field("Número único de identificación", "numero_identificacion")
        add_field("Fecha de nacimiento", "fecha_nacimiento", input_type="date")
        add_field("Edad gestacional al nacer (semanas)", "edad_gestacional")
        add_field("Sexo", "sexo", input_type="combo")
        add_field("Peso al nacer (g)", "peso")
        add_field("Longitud al nacer (cm)", "longitud")
        add_field("Perímetro cefálico (cm)", "pc")

        boton_guardar = QPushButton("Guardar")
        boton_guardar.clicked.connect(self.guardar)
        layout.addWidget(boton_guardar)

    def clasificar_peso(self, edad_gestacional, peso):
        if edad_gestacional < 24 or edad_gestacional > 42 or peso <= 0:
            return "Datos no válidos"

        # Lógica aproximada basada en tabla Fenton (ajustar si tienes referencia exacta)
        if edad_gestacional >= 24 and edad_gestacional <= 42:
            if edad_gestacional <= 37 and peso < 2500:
                return "PEG (pequeño para edad gestacional)"
            elif peso >= 4000:
                return "GEG (grande para edad gestacional)"
            else:
                return "AEG (adecuado para edad gestacional)"
        return "Desconocido"

    def guardar(self):
        try:
            db = SessionLocal()

            identificacion = self.fields["numero_identificacion"].text().strip()
            existente = db.query(PacienteNeonato).filter_by(numero_identificacion=identificacion).first()
            if existente:
                QMessageBox.warning(self, "Duplicado", "Ya existe un neonato con ese número de identificación.")
                return

            edad_gestacional = int(self.fields["edad_gestacional"].text())
            peso = int(self.fields["peso"].text())
            clasificacion = self.clasificar_peso(edad_gestacional, peso)

            nuevo = PacienteNeonato(
                nombre=self.fields["nombre"].text(),
                numero_identificacion=identificacion,
                fecha_nacimiento=self.fields["fecha_nacimiento"].date().toPython(),
                edad_semanas=edad_gestacional,
                sexo=self.fields["sexo"].currentText(),
                peso=peso,
                talla=float(self.fields["longitud"].text()),
                pc=float(self.fields["pc"].text()),
                clasificacion_peso=clasificacion,
                usuario_id=self.usuario_id
            )

            db.add(nuevo)
            db.commit()
            QMessageBox.information(self, "Éxito", "Neonato registrado correctamente.")
            self.close()
        except Exception as e:
            db.rollback()
            QMessageBox.critical(self, "Error", f"No se pudo registrar: {e}")
        finally:
            db.close()


if __name__ == "__main__":
    app = QApplication([])
    win = RegistrarNeonatoWindow()
    win.show()
    app.exec()
