# Inicializa SQLAlchemy para la aplicación Flask

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    """Inicializa la instancia de SQLAlchemy con la aplicación Flask."""
    db.init_app(app)

# Importar los modelos después de crear la instancia de SQLAlchemy
from .user import User
from .game import Game
from .user_game_score import UserGameScore
