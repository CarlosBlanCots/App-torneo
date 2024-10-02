# Inicializa y registra los blueprints para las rutas

# Crear blueprints para cada conjunto de rutas
from .auth_routes import auth_bp
from .user_routes import user_bp
from .admin_routes import admin_bp

# Registrar los blueprints en la aplicación
def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
