from . import db
from sqlalchemy.orm import relationship

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    users = relationship('User', secondary='user_games', back_populates='games')

    def __repr__(self):
        return f'<Game {self.name}>'
