from flask_wtf import FlaskForm
from wtforms import SubmitField

# Erstellt eine Basisformularklasse, die von FlaskForm erbt.
class BaseForm(FlaskForm):
    # Definiert den Submit-Button mit einem neutralen Button-Stil.
    submit = SubmitField("Submit", render_kw={"class": "btn btn-neutral"})
