from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from . import db
from .user_games import user_games

class User(db.Model, UserMixin):
    """
    Modelo para representar un usuario en la base de datos.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)

    # Relación con la tabla de juegos a través de la tabla secundaria user_games
    games = relationship("Game", secondary=user_games, back_populates="users")

    def set_password(self, password):
        """
        Configura el hash de la contraseña para el usuario.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifica la contraseña proporcionada contra el hash almacenado.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Representa el usuario como una cadena.
        """
        return f'<User {self.username}>'