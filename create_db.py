from app import app
from models import db

with app.app_context():
    db.create_all()  # Esto creará las tablas en la base de datos.
