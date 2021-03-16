from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class MealOrder(FlaskForm):
    klass = StringField('Класс с литерой',validators=[DataRequired()])
    bufet = IntegerField('Количество порций',validators=[DataRequired()])
    hot_meal = IntegerField('Количество порций', validators=[DataRequired()])
    submit = SubmitField('Отправить заявку')