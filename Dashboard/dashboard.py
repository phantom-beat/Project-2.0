import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt

class DashboardWindow(QMainWindow):
    def __init__(self, user_name="Dra. Ana Ruiz"):
        super().__init__()
        self.setWindowTitle("NutriClinicIMB - Dashboard")
        self.setGeometry(100, 100, 1000, 600)

        # Widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- Barra Lateral (Izquierda) ---
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #f5f5f5; padding: 10px; color: #333;")
        sidebar_layout = QVBoxLayout(sidebar)

        # Título de la barra lateral
        sidebar_title = QLabel("NutriClinicIMB")
        sidebar_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 20px; color: #333;")
        sidebar_layout.addWidget(sidebar_title)

        # Opciones de la barra lateral
        menu_items = [
            ("Registrar medidas", "📝"),
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
            if text == "Cerrar sesión":
                btn.clicked.connect(self.close)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # --- Contenido Principal (Derecha) ---
        content = QWidget()
        content_layout = QVBoxLayout(content)

        # Encabezado
        greeting = QLabel(f"Bienvenid@, {user_name}")
        greeting.setStyleSheet("color: #333; font-size: 20px; font-weight: bold; margin: 10px 0;")
        content_layout.addWidget(greeting)

        subtitle = QLabel("Su plataforma para la gestión nutricional de neonatos y niños")
        subtitle.setStyleSheet("color: #666; font-size: 14px; margin-bottom: 20px;")
        content_layout.addWidget(subtitle)

        # Botones de acción
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)

        register_button = QPushButton("Registrar medidas antropométricas")
        register_button.setStyleSheet("""
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
        button_layout.addWidget(register_button)

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
        button_layout.addWidget(report_button)

        button_layout.addStretch()
        content_layout.addWidget(button_container)

        # Enlace "Añadir nuevo paciente"
        add_patient = QPushButton("Añadir nuevo paciente")
        add_patient.setStyleSheet("""
            QPushButton {
                color: #007BFF;
                font-size: 14px;
                background: none;
                border: none;
                padding: 5px 0;
                text-align: left;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        add_patient.setCursor(Qt.PointingHandCursor)
        content_layout.addWidget(add_patient)

        # Tabla de pacientes recientes
        patients_label = QLabel("Pacientes Recientes")
        patients_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px 0;")
        content_layout.addWidget(patients_label)

        table = QTableWidget()
        table.setRowCount(5)
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Nombre del Paciente", "Fecha de Nacimiento", "Edad", "Sexo", "Acciones"])
        table.setStyleSheet("border: 1px solid #ccc;")

        # Datos de ejemplo
        patients_data = [
            ("Santiago Silva", "1986-07-15", "38", "Masculino"),
            ("Sofía Morales", "1995-01-22", "30", "Femenino"),
            ("Mateo Pérez", "2005-05-10", "19", "Masculino"),
            ("Isabella Gómez", "2000-11-01", "24", "Femenino"),
            ("Lucía Fernandez", "2007-02-28", "18", "Femenino")
        ]

        for row, (name, dob, age, sex) in enumerate(patients_data):
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(dob))
            table.setItem(row, 2, QTableWidgetItem(age))
            table.setItem(row, 3, QTableWidgetItem(sex))
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
            table.setCellWidget(row, 4, details_btn)

        # Ajustar el tamaño de las columnas
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setEditTriggers(QTableWidget.NoEditTriggers)  # Hacer la tabla no editable
        content_layout.addWidget(table)

        # Footer
        footer = QLabel("NutriClinicIMB - 2025")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: gray; font-size: 12px; margin-top: 20px;")
        content_layout.addWidget(footer)

        main_layout.addWidget(content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())