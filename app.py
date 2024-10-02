# Este archivo inicializa la aplicación Flask, configura las extensiones y registra las rutas principales

from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from models import db
from models.user import User
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp

# Inicializa la aplicación Flask con la configuración definida en Config
app = Flask(__name__)
app.config.from_object(Config)

# Inicializa la base de datos con la aplicación
db.init_app(app)

# Crea las tablas en la base de datos si no existen
with app.app_context():
    db.create_all()

# Inicializa el manejador de sesiones para gestionar la autenticación de usuarios
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Establece la vista de login

# Carga el usuario activo desde la base de datos por su ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registra los blueprints de las rutas de autenticación, usuario y administrador
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')

# Redirige a la página de inicio de sesión cuando se accede a la raíz del sitio
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

# Ejecuta la aplicación en modo de depuración
if __name__ == '__main__':
    app.run(debug=True)
