from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, SelectMultipleField, IntegerField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

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


class AdminRegistrationForm(FlaskForm):
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
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    is_admin = BooleanField('Administrador')
    games = SelectMultipleField(
        'Selecciona Juegos',
        choices=[],
        validators=[Optional()]
    )
    submit = SubmitField('Guardar Cambios')



class GameSelectionForm(FlaskForm):
    games = SelectMultipleField(
        'Selecciona los juegos',
        choices=[],  # Inicializamos la lista de opciones vacía
        validators=[DataRequired(message="Debes seleccionar al menos un juego")]
    )
    submit = SubmitField('Guardar Selección')


class GameForm(FlaskForm):
    name = StringField('Nombre del Juego', validators=[DataRequired()])
    rules = TextAreaField('Reglas del Juego')
    submit = SubmitField('Añadir Juego')

class RulesForm(FlaskForm):
    rules = TextAreaField(
        'Reglas del Torneo',
        validators=[DataRequired(message="Este campo es obligatorio.")]
    )
    submit = SubmitField('Guardar Reglas')
