
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Importar rutas
from routes.patients import patients_bp
from routes.nutrition import nutrition_bp

app.register_blueprint(patients_bp, url_prefix="/api/patients")
app.register_blueprint(nutrition_bp, url_prefix="/api/nutrition")

if __name__ == "__main__":
    app.run(debug=True)