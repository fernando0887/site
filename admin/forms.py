from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    name= StringField('Nome', [validators.Length(min=3, max=50)])
    username= StringField('Nome de usúario', [validators.Length(min=3, max=50)])
    email= StringField('Endereço de email', [validators.Length(min=6, max=50)])
    password= PasswordField('Nova senha', [validators.DataRequired(), validators.EqualTo('confirm', message='Deve ser a mesma do campo anterior')])
    confirm= PasswordField('Repita a senha')
   
 

class LoginFormulario(Form): 
     email= StringField('Endereço de email', [validators.Length(min=6, max=50)])
     password= PasswordField('Senha', [validators.DataRequired()])