from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from models import db
from models.user import User
from models.game import Game
from models.user_game_score import user_games
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp

# Inicializa la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializa las extensiones
db.init_app(app)

# Crea las tablas si no existen
with app.app_context():
    db.create_all()

# Inicializa el LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Define el nombre de la vista de login

# Carga el usuario para la sesión
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registra los blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
