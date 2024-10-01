from . import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

# Modelo para almacenar la puntuación de los usuarios en los juegos
class UserGameScore(db.Model):
    __tablename__ = 'user_game_scores'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    score = Column(Integer, default=0)  # Puntuación del usuario para el juego

    # Relación con User y Game
    user = relationship('User', back_populates='game_scores')
    game = relationship('Game', back_populates='user_scores')
