from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, URL, NumberRange, ValidationError
from database.models import Post, Journal  # Asegúrate de importar tus modelos Post y Journal


class LoginForm(FlaskForm):
    name = StringField(label="User Name:", validators=[InputRequired(), Length(min=4, max=100)])
    password = PasswordField(label="Password:", validators=[InputRequired(), Length(min=8, max=100)])
    submit = SubmitField(label="Sign in")


class PostForm(FlaskForm):
    author = StringField(label="Autor", validators=[InputRequired(), Length(min=1, max=100)])
    title = StringField(label="Título", validators=[InputRequired(), Length(min=1, max=250)])
    image = StringField(label="URL de Imagen", validators=[InputRequired(), Length(max=250)])
    content = TextAreaField(label="Contenido", validators=[InputRequired()])
    category = StringField(label="Categoría", validators=[InputRequired(), Length(min=1, max=100)])
    slug = StringField(label="Slug", validators=[InputRequired(), Length(min=1, max=100)])
    submit = SubmitField(label="Crear Nuevo Post")

    def validate_image(form, field):
        if not field.data.startswith(('http://', 'https://')):
            raise ValidationError('Formato de URL no válido para imagen. Debe de empezar con http:// or https://')


class JournalForm(FlaskForm):
    date = DateTimeField(label="Fecha", validators=[InputRequired()], format='%Y-%m-%dT%H:%M')  # Use the format for datetime-local input
    number = IntegerField(label="Número", validators=[InputRequired(), NumberRange(min=1)])
    year = IntegerField(label="Año", validators=[InputRequired(), NumberRange(min=2000, max=2100)])
    title = StringField(label="Título", validators=[InputRequired(), Length(min=1, max=250)])
    url = StringField(label="URL", validators=[InputRequired(), Length(max=250), URL()])
    image = StringField(label="URL de Imagen", validators=[Length(max=250), URL()])
    submit = SubmitField(label="Crear Nuevo Journal")

    def validate_image(form, field):
        if field.data and not field.data.startswith(('http://', 'https://')):
            raise ValidationError('Formato de URL no válido para imagen. Debe de empezar con http:// o https://')
