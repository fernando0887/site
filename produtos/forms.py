from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField


class Addprodutos(Form):
    name= StringField('Nome do produto:', [validators.DataRequired()])
    price= DecimalField('Preço:', [validators.DataRequired()])
    discount= IntegerField('Desconto:', [validators.DataRequired()])
    stock= IntegerField('Quantidade:', [validators.DataRequired()])
    discription= TextAreaField('Descrição:', [validators.DataRequired()])
    colors= TextAreaField('Variante:', [validators.DataRequired()])
    img_1= FileField('Imagem do produto:', validators=[FileRequired(),FileAllowed(['jpg','png','gif','jpeg'])])
    img_2= FileField('Imagem do produto:', validators=[FileRequired(),FileAllowed(['jpg','png','gif','jpeg'])])
    img_3= FileField('Imagem do produto:', validators=[FileRequired(),FileAllowed(['jpg','png','gif','jpeg'])])
