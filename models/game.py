# Define el modelo Game para la base de datos

from . import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Game(db.Model):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    rules = db.Column(db.Text, nullable=True)

    # Relación con UserGameScore para gestionar puntuaciones
    user_scores = relationship('UserGameScore', back_populates='game')
