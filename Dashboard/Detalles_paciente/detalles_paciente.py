from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from database.db import SessionLocal
from models.medicion import Medicion

class DetallesPacienteWindow(QMainWindow):
    def __init__(self, paciente):
        super().__init__()
        self.setWindowTitle("Detalles del Paciente")
        self.setGeometry(200, 200, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Obtener identificación del paciente (soporta paciente normal y neonato si luego se unifica)
        ident = getattr(paciente, 'cedula', None) or getattr(paciente, 'numero_identificacion', 'Sin ID')

        label = QLabel(f"Historial de mediciones de {paciente.nombre} (ID: {ident})")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(label)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Fecha", "Altura", "Peso", "Cintura", "Cadera", "IMC"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.cargar_mediciones(ident)

    def cargar_mediciones(self, cedula):
        db = SessionLocal()
        try:
            mediciones = db.query(Medicion).filter_by(patient_id=cedula).order_by(Medicion.date.desc()).all()
            self.table.setRowCount(len(mediciones))

            for row, m in enumerate(mediciones):
                imc = round(m.weight / ((m.height / 100) ** 2), 2) if m.height and m.weight else "-"
                self.table.setItem(row, 0, QTableWidgetItem(str(m.date)))
                self.table.setItem(row, 1, QTableWidgetItem(str(m.height)))
                self.table.setItem(row, 2, QTableWidgetItem(str(m.weight)))
                self.table.setItem(row, 3, QTableWidgetItem(str(m.waist)))
                self.table.setItem(row, 4, QTableWidgetItem(str(m.hip)))
                self.table.setItem(row, 5, QTableWidgetItem(str(imc)))
        except Exception as e:
            print(f"Error cargando mediciones: {e}")
        finally:
            db.close()
