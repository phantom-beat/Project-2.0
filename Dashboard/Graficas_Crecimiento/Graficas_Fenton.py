from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
)
from PySide6.QtCore import Qt
from database.db import SessionLocal
from models.paciente_neonato import PacienteNeonato

class GraficasCrecimientoWindow(QMainWindow):
    def __init__(self, usuario_id):
        super().__init__()
        self.usuario_id = usuario_id
        self.setWindowTitle("Gráficas de Crecimiento - Neonatos")
        self.setGeometry(200, 200, 900, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        title = QLabel("Neonatos Registrados")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Nombre", "Identificación", "Fecha de Nacimiento", 
            "Edad gestacional", "Sexo", "Acciones"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.cargar_neonatos()

    def cargar_neonatos(self):
        db = SessionLocal()
        try:
            neonatos = db.query(PacienteNeonato).filter_by(usuario_id=self.usuario_id).all()
            self.table.setRowCount(len(neonatos))

            for row, neonato in enumerate(neonatos):
                self.table.setItem(row, 0, QTableWidgetItem(neonato.nombre))
                self.table.setItem(row, 1, QTableWidgetItem(neonato.numero_identificacion))
                self.table.setItem(row, 2, QTableWidgetItem(str(neonato.fecha_nacimiento)))
                self.table.setItem(row, 3, QTableWidgetItem(str(neonato.edad_semanas)))
                self.table.setItem(row, 4, QTableWidgetItem(neonato.sexo))

                # Botones de acción
                btn_detalles = QPushButton("Ver detalles")
                btn_detalles.clicked.connect(lambda _, n=neonato: self.ver_detalles(n))

                btn_grafica = QPushButton("Generar gráfica")
                btn_grafica.clicked.connect(lambda _, n=neonato: self.generar_grafica(n))

                contenedor = QWidget()
                acciones = QVBoxLayout(contenedor)
                acciones.addWidget(btn_detalles)
                acciones.addWidget(btn_grafica)
                acciones.setContentsMargins(0, 0, 0, 0)
                self.table.setCellWidget(row, 5, contenedor)

        except Exception as e:
            print(f"Error al cargar neonatos: {e}")
        finally:
            db.close()

    def ver_detalles(self, neonato):
        print(f"Ver detalles de {neonato.nombre} - Clasificación: {neonato.clasificacion_peso}")
        # Aquí se implementará la ventana de detalles

    def generar_grafica(self, neonato):
        print(f"Generar gráfica de crecimiento para {neonato.nombre}")
        # Aquí se implementará la ventana con la gráfica de Fenton
