from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from models import Game

class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Este campo es obligatorio"),
            Email(message="Introduce un email válido")
        ]
    )
    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(message="Este campo es obligatorio")]
    )
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    username = StringField(
        'Nombre de Usuario',
        validators=[
            DataRequired(message="Este campo es obligatorio"),
            Length(
                min=2,
                max=20,
                message="El nombre debe tener entre 2 y 20 caracteres"
            )
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Este campo es obligatorio"),
            Email(message="Introduce un email válido")
        ]
    )
    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message="Este campo es obligatorio"),
            Length(min=6, message="La contraseña debe tener al menos 6 caracteres")
        ]
    )
    confirm_password = PasswordField(
        'Confirmar Contraseña',
        validators=[
            DataRequired(message="Este campo es obligatorio"),
            EqualTo('password', message="Las contraseñas no coinciden")
        ]
    )
    games = SelectMultipleField(
        'Selecciona los juegos en los que participarás',
        choices=[],  # Inicializamos la lista de opciones vacía
        validators=[DataRequired(message="Debes seleccionar al menos un juego")]  # Aquí se agrega el validador
    )
    submit = SubmitField('Registrar')

class GameScoreForm(FlaskForm):
    game = StringField('Juego', render_kw={'readonly': True})  # Campo solo lectura
    score = IntegerField('Puntuación', default=0)

class EditUserForm(FlaskForm):
    username = StringField(
        'Nombre de Usuario',
        validators=[
            DataRequired(message="Este campo es obligatorio"),
            Length(min=2, max=20, message="El nombre debe tener entre 2 y 20 caracteres")
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Este campo es obligatorio"),
            Email(message="Introduce un email válido")
        ]
    )
    password = PasswordField('Contraseña', validators=[Optional()])
    confirm_password = PasswordField(
        'Confirmar Contraseña',
        validators=[
            Optional(),
            EqualTo('password', message="Las contraseñas no coinciden")
        ]
    )
    is_admin = BooleanField('Administrador')

    # Lista de juegos y puntuaciones asociadas (usando FieldList y FormField)
    game_scores = FieldList(FormField(GameScoreForm), min_entries=0)

    submit = SubmitField('Guardar Cambios')

class GameSelectionForm(FlaskForm):
    games = SelectMultipleField(
        'Selecciona los juegos',
        choices=[],  # Inicializamos la lista de opciones vacía
        validators=[DataRequired(message="Debes seleccionar al menos un juego")]
    )
    submit = SubmitField('Guardar Selección')
