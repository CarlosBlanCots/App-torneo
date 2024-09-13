from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def init_app(app):
    """Inicializa la instancia de SQLAlchemy con la aplicación Flask."""
    db.init_app(app)