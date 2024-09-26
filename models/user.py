from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)

    # Relación con UserGameScore para gestionar los juegos y puntuaciones
    game_scores = relationship('UserGameScore', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
