# Este archivo define los formularios utilizados en la aplicación.

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, SelectMultipleField, IntegerField, FieldList
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class LoginForm(FlaskForm):
    # Formulario para iniciar sesión.
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


class AdminRegistrationForm(FlaskForm):
    # Formulario para registrar un nuevo administrador.
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
    submit = SubmitField('Registrar')


class RegistrationForm(FlaskForm):
    # Formulario para registrar un nuevo usuario.
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
        validators=[DataRequired(message="Debes seleccionar al menos un juego")]
    )
    submit = SubmitField('Registrar')

class EditUserForm(FlaskForm):
    # Formulario para editar los datos de un usuario.
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    is_admin = BooleanField('Administrador')
    games = SelectMultipleField(
        'Selecciona Juegos',
        choices=[],
        validators=[Optional()]
    )
    scores = FieldList(IntegerField('Puntuación'), min_entries=0)  # Agrega un campo de lista para las puntuaciones
    submit = SubmitField('Guardar Cambios')

class GameSelectionForm(FlaskForm):
    # Formulario para seleccionar juegos.
    games = SelectMultipleField(
        'Selecciona los juegos',
        choices=[],  # Inicializamos la lista de opciones vacía
        validators=[DataRequired(message="Debes seleccionar al menos un juego")]
    )
    submit = SubmitField('Guardar Selección')

class GameForm(FlaskForm):
    # Formulario para añadir un nuevo juego.
    name = StringField('Nombre del Juego', validators=[DataRequired()])
    rules = TextAreaField('Reglas del Juego')
    submit = SubmitField('Añadir Juego')

class RulesForm(FlaskForm):
    # Formulario para guardar las reglas del torneo.
    rules = TextAreaField(
        'Reglas del Torneo',
        validators=[DataRequired(message="Este campo es obligatorio.")]
    )
    submit = SubmitField('Guardar Reglas')
