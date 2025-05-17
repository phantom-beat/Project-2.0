import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
from database.db import SessionLocal
from models.paciente import Paciente

# Asegurar acceso al proyecto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from Dashboard.Registrar_Paciente.registrar_paciente import RegistrarUsuarioWindow
from Dashboard.Detalles_paciente.detalles_paciente import DetallesPacienteWindow
from Dashboard.Registrar_paciente_neonato.Registrar_neonato import RegistrarNeonatoWindow
from Dashboard.Graficas_Crecimiento.Graficas_Fenton import GraficasCrecimientoWindow


class DashboardWindow(QMainWindow):
    def __init__(self, user_id, user_name=""):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name
        self.setWindowTitle("NutriClinicIMB - Dashboard")
        self.setGeometry(100, 100, 1000, 600)

        # Layout general
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- Menú lateral ---
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #f5f5f5; padding: 10px; color: #333;")
        sidebar_layout = QVBoxLayout(sidebar)

        sidebar_title = QLabel("NutriClinicIMB")
        sidebar_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 20px; color: #333;")
        sidebar_layout.addWidget(sidebar_title)

        menu_items = [
            ("Registrar pacientes", "📝"),
            ("Crear plan alimenticio", "🍽️"),
            ("Ver informes", "📄"),
            ("Gráficas de crecimiento", "📈"),
            ("Cerrar sesión", "❌")
        ]

        for text, icon in menu_items:
            btn = QPushButton(f"{icon}  {text}")
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 10px;
                    font-size: 14px;
                    background: none;
                    border: none;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            btn.setCursor(Qt.PointingHandCursor)

            if text == "Registrar pacientes":
                btn.clicked.connect(self.abrir_ventana_registro)
            elif text == "Gráficas de crecimiento":
                btn.clicked.connect(self.abrir_graficas_crecimiento)
            elif text == "Cerrar sesión":
                btn.clicked.connect(self.close)

            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # --- Área de contenido principal ---
        content = QWidget()
        content_layout = QVBoxLayout(content)

        greeting = QLabel(f"Bienvenid@, {user_name}")
        greeting.setStyleSheet("color: #333; font-size: 20px; font-weight: bold; margin: 10px 0;")
        content_layout.addWidget(greeting)

        subtitle = QLabel("Su plataforma para la gestión nutricional")
        subtitle.setStyleSheet("color: #666; font-size: 14px; margin-bottom: 20px;")
        content_layout.addWidget(subtitle)

        # Botón "Añadir nuevo paciente"
        add_patient_button = QPushButton("➕ Añadir nuevo paciente")
        add_patient_button.setStyleSheet("""
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
        add_patient_button.setCursor(Qt.PointingHandCursor)
        add_patient_button.clicked.connect(self.abrir_ventana_registro)
        content_layout.addWidget(add_patient_button)

        # Botón registro neonatos
        neonatos_button = QPushButton("Registro de neonatos")
        neonatos_button.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: black;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        neonatos_button.setCursor(Qt.PointingHandCursor)
        neonatos_button.clicked.connect(self.abrir_ventana_neonatos)
        content_layout.addWidget(neonatos_button)

        # Botón "Generar informe"
        report_button = QPushButton("Generar informe")
        report_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #007BFF;
                padding: 10px;
                font-size: 14px;
                border: 1px solid #007BFF;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        content_layout.addWidget(report_button)

        # Tabla de pacientes
        patients_label = QLabel("Pacientes Recientes")
        patients_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px 0;")
        content_layout.addWidget(patients_label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Nombre del Paciente", "Fecha de Nacimiento", "Edad", "Sexo", "Acciones"])
        self.table.setStyleSheet("border: 1px solid #ccc;")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        content_layout.addWidget(self.table)

        self.actualizar_tabla_pacientes()

        # Footer
        footer = QLabel("NutriclinicIMB - 2025")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: gray; font-size: 12px; margin-top: 20px;")
        content_layout.addWidget(footer)

        main_layout.addWidget(content)

    def abrir_ventana_registro(self):
        self.registro_window = RegistrarUsuarioWindow(usuario_id=self.user_id)
        self.registro_window.paciente_registrado.connect(self.agregar_paciente)
        self.registro_window.show()

    def abrir_ventana_neonatos(self):
        self.neonato_window = RegistrarNeonatoWindow(usuario_id=self.user_id)
        self.neonato_window.show()

    def abrir_graficas_crecimiento(self):
        self.graficas_window = GraficasCrecimientoWindow(usuario_id=self.user_id)
        self.graficas_window.show()

    def agregar_paciente(self, paciente):
        self.pacientes.insert(0, paciente)
        self.actualizar_tabla_pacientes()

    def actualizar_tabla_pacientes(self):
        db = SessionLocal()
        self.pacientes = db.query(Paciente).filter_by(usuario_id=self.user_id).all()
        db.close()

        self.table.setRowCount(len(self.pacientes))
        for row, paciente in enumerate(self.pacientes):
            self.table.setItem(row, 0, QTableWidgetItem(paciente.nombre))
            self.table.setItem(row, 1, QTableWidgetItem(paciente.fecha_nacimiento.strftime("%Y-%m-%d")))
            self.table.setItem(row, 2, QTableWidgetItem(str(paciente.edad)))
            self.table.setItem(row, 3, QTableWidgetItem(paciente.sexo))
            details_btn = QPushButton("Ver detalles")
            details_btn.setStyleSheet("""
                QPushButton {
                    color: #007BFF;
                    background: none;
                    border: none;
                }
                QPushButton:hover {
                    text-decoration: underline;
                }
            """)
            details_btn.clicked.connect(lambda _, p=paciente: self.abrir_detalles_paciente(p))
            self.table.setCellWidget(row, 4, details_btn)

    def abrir_detalles_paciente(self, paciente):
        self.detalle_window = DetallesPacienteWindow(paciente)
        self.detalle_window.show()
        self.detalle_window.raise_()
        self.detalle_window.activateWindow()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow(user_id=1, user_name="Admin")  # Esto es para pruebas
    window.show()
    sys.exit(app.exec())
