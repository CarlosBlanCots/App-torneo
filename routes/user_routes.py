# user_routes.py: Define las rutas y la lógica para el usuario autenticado, incluyendo el perfil y las comparativas.

from flask import Blueprint, render_template, session, request
from flask_login import login_required, current_user
from models import User, Game, UserGameScore

user_bp = Blueprint('user', __name__)

@user_bp.route('/home')
@login_required
def home():
    # Renderiza la página de inicio del usuario con los rankings de juegos.
    rankings = get_rankings()
    return render_template('home.html', rankings=rankings)

def get_rankings():
    # Obtiene y organiza los rankings de todos los juegos.
    games = Game.query.all()

    rankings = []
    for game in games:
        scores = (UserGameScore.query
                  .filter_by(game_id=game.id)
                  .order_by(UserGameScore.score.desc())
                  .all())

        game_ranking = []
        for i, score in enumerate(scores, start=1):
            user = User.query.get(score.user_id)
            game_ranking.append({
                'position': i,
                'username': user.username,
                'score': score.score
            })

        rankings.append({
            'game': game.name,
            'ranking': game_ranking
        })

    return rankings

@user_bp.route('/perfil')
@login_required
def user_data():
    # Muestra los datos del usuario y sus puntuaciones en los juegos.
    user_game_scores = current_user.game_scores

    rankings = {}
    for user_game in user_game_scores:
        ranking_scores = UserGameScore.query.filter_by(game_id=user_game.game_id).order_by(UserGameScore.score.desc()).all()
        position = next((index + 1 for index, ranked_user_game in enumerate(ranking_scores) if ranked_user_game.user_id == current_user.id), None)
        rankings[user_game.game_id] = position if position else '-'

    return render_template('user_data.html', user_game_scores=user_game_scores, rankings=rankings)

@user_bp.route('/reglas', methods=['GET'])
@login_required
def rules():
    # Muestra las reglas del torneo almacenadas en la sesión.
    reglas_torneo = session.get('reglas_torneo', [])
    return render_template('rules.html', reglas=reglas_torneo)

@user_bp.route('/participants', methods=['GET'])
@login_required
def participants():
    # Muestra la lista de todos los participantes en el torneo.
    users = User.query.all()
    return render_template('participants.html', users=users)

@user_bp.route('/comparativa', methods=['GET', 'POST'])
@login_required
def comparison():
    # Permite comparar las puntuaciones entre dos jugadores en un juego específico.
    users = User.query.all()
    games = Game.query.all()

    if request.method == 'POST':
        player1_id = request.form['player1_id']
        player2_id = request.form['player2_id']
        game_id = request.form['game_id']

        player1_scores = UserGameScore.query.filter_by(user_id=player1_id, game_id=game_id).all()
        player2_scores = UserGameScore.query.filter_by(user_id=player2_id, game_id=game_id).all()

        scores_by_date_player1 = {}
        scores_by_date_player2 = {}

        for score in player1_scores:
            date = score.date.date()
            if date not in scores_by_date_player1:
                scores_by_date_player1[date] = []
            scores_by_date_player1[date].append(score.score)

        for score in player2_scores:
            date = score.date.date()
            if date not in scores_by_date_player2:
                scores_by_date_player2[date] = []
            scores_by_date_player2[date].append(score.score)

        date_labels = sorted(set(scores_by_date_player1.keys()).union(scores_by_date_player2.keys()))
        max_scores_player1 = [max(scores_by_date_player1.get(date, [0])) for date in date_labels]
        max_scores_player2 = [max(scores_by_date_player2.get(date, [0])) for date in date_labels]

        return render_template('comparison.html', date_labels=date_labels, max_scores_player1=max_scores_player1, max_scores_player2=max_scores_player2, games=games, users=users)

    return render_template('comparison.html', games=games, users=users)
