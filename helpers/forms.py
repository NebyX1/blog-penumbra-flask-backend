from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError


class LoginForm(FlaskForm):
    name = StringField(label="User Name:", validators=[InputRequired(), Length(min=4, max=100)])
    password = PasswordField(label="Password:", validators=[InputRequired(), Length(min=8, max=100)])
    submit = SubmitField(label="Sign in")


class PostForm(FlaskForm):
    author = StringField(label="Author", validators=[InputRequired(), Length(min=1, max=100)])
    title = StringField(label="Title", validators=[InputRequired(), Length(min=1, max=250)])
    image = StringField(label="Image URL", validators=[InputRequired(), Length(max=250)])
    content = TextAreaField(label="Content", validators=[InputRequired()])
    submit = SubmitField(label="Create Post")

    def validate_image(form, field):
        if not field.data.startswith(('http://', 'https://')):
            raise ValidationError('Invalid URL format for image. Must start with http:// or https://')
