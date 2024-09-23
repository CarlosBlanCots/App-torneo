from app import app  # Importa la instancia de la aplicación directamente
from models import db
from models.game import Game  # Importa el modelo Game desde el archivo correcto

def add_initial_games():
    # Crea una lista de juegos
    games = [
        Game(name='Tetris'),
        Game(name='Pac-man'),
        Game(name='Street Fighter II')
    ]

    # Añadir los juegos a la base de datos
    with app.app_context():
        for game in games:
            db.session.add(game)

        db.session.commit()
        print('Juegos añadidos exitosamente.')

if __name__ == '__main__':
    add_initial_games()
