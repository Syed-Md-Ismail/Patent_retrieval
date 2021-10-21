from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length




class InputTextForm(FlaskForm):
    input_text = StringField('InputText',
                              validators=[DataRequired(), Length(min=2, max=1000)])
    search_button = SubmitField('Search')
    
