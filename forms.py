from wtforms import Form, SubmitField, IntegerField, FloatField,StringField,TextAreaField, validators, PasswordField, ValidationError
from flask_wtf.file import FileField, FileRequired,FileAllowed
from flask_wtf import FlaskForm
from.models import Cadastrar
import email_validator


class CadastroClienteForm(FlaskForm):
    name= StringField('Nome:')
    username= StringField('Usúario:', [validators.DataRequired()])
    rg= StringField('RG:', [validators.DataRequired()])
    cpf= StringField('CPF:', [validators.DataRequired()])
    birth= StringField('Nascimento:', [validators.DataRequired()])
    email= StringField('Email:', [validators.Email(),validators.DataRequired()])
    password= PasswordField('Senha:', [validators.DataRequired(), validators.EqualTo('confirm', message= 'As duas senhas devem ser iguais!')])
    confirm= PasswordField('Redigite a senha:', [validators.DataRequired()])
    country= StringField('País:', [validators.DataRequired()])
    city= StringField('Cidade:', [validators.DataRequired()])
    contact= StringField('Telefone com DDD:', [validators.DataRequired()])
    address= StringField('Endereço:', [validators.DataRequired()])
    district= StringField('Bairro:', [validators.DataRequired()])
    state= StringField('Estado:', [validators.DataRequired()])
    zipcode= StringField('CEP:', [validators.DataRequired()])
    profile= FileField('Foto:', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Apenas fotos!')])

    submit= SubmitField('Cadastrar')


def validate_username(self, username):
    if Cadastrar.query.filter_by(username=username.data).first():
        raise ValidationError('Este úsuario já esta sendo usado!')


def validate_email(self, email):
    if Cadastrar.query.filter_by(email=email.data).first():
        raise ValidationError('Este email já esta sendo usado!')


class ClienteLoginForm(FlaskForm):
    email= StringField('Email:', [validators.Email(),validators.DataRequired()])
    password= PasswordField('Senha:', [validators.DataRequired()])
    
    