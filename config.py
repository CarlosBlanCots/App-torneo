# Configuración de la aplicación para el proyecto de torneo de videojuegos.

import os
from datetime import timedelta

class Config:
    # Configuración base para la aplicación, incluyendo la clave secreta y la URI de la base de datos.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tournament.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
