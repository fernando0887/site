from email.policy import default
from unicodedata import name
from loja import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json

import loja



class JsonEncodedDict(db.TypeDecorator):
    impl= db.Text


    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)    

    
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)    


@login_manager.user_loader

def carregar_user(user_id):
    return Cadastrar.query.get(user_id)

class Cadastrar(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key = True)
    name= db.Column(db.String(60), unique = False)
    username= db.Column(db.String(60), unique = False)
    rg= db.Column(db.String(60), unique = True)
    cpf= db.Column(db.String(60), unique = True)
    birth= db.Column(db.String(10), unique = False)
    email= db.Column(db.String(60), unique = False)
    password= db.Column(db.String(60), unique = False)
    country= db.Column(db.String(60), unique = False)
    state= db.Column(db.String(60), unique = False)
    city= db.Column(db.String(60), unique = False)
    contact= db.Column(db.String(60), unique = False)
    address= db.Column(db.String(60), unique = False)
    district= db.Column(db.String(60), unique = False)
    zipcode= db.Column(db.String(60), unique = False)
    profile= db.Column(db.String(60), unique = False, default= 'profile.jpg')
    data= db.Column(db.DateTime, nullable = False, default= datetime.utcnow)

    def __repr__(self):
        return '<Cadastrar %r>' % self.name


class ClientePedido(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    notafiscal= db.Column(db.String(20), unique = True, nullable = False )
    status= db.Column(db.String(20), default= 'pendente', nullable = False)
    cliente_id= db.Column(db.Integer, unique = False, nullable= False)
    data_criado= db.Column(db.DateTime, nullable = False, default= datetime.utcnow)
    pedido= db.Column(JsonEncodedDict)

    def __repr__(self):
        return '<ClientePedido %r>' % self.notafiscal



db.create_all()     
