conn = sqlite3.connect('antropometricas.db')
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER NOT NULL,
    peso REAL NOT NULL,
    altura REAL NOT NULL,
    imc REAL NOT NULL
)
''')
conn.commit()

# Función para calcular el IMC
def calcular_imc(peso, altura):
    return round(peso / (altura ** 2), 2)

# Función para guardar los datos
def guardar_datos():
    nombre = entry_nombre.get()
    edad = entry_edad.get()
    peso = entry_peso.get()
    altura = entry_altura.get()

    if not (nombre and edad and peso and altura):
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    try:
        edad = int(edad)
        peso = float(peso)
        altura = float(altura)
        imc = calcular_imc(peso, altura)

        cursor.execute('''
        INSERT INTO pacientes (nombre, edad, peso, altura, imc)
        VALUES (?, ?, ?, ?, ?)
        ''', (nombre, edad, peso, altura, imc))
        conn.commit()

        messagebox.showinfo("Éxito", "Datos guardados correctamente")
        entry_nombre.delete(0, 'end')
        entry_edad.delete(0, 'end')
        entry_peso.delete(0, 'end')
        entry_altura.delete(0, 'end')
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos")
