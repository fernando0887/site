from flask import flash, redirect, render_template, session, request, url_for,flash
from loja import app, db, bcrypt
from loja.produtos.models import Addproduto,Marcas,Categoria  
from .forms import LoginFormulario, RegistrationForm
from .models import User
import os


@app.route('/admin')

def admin():
    if 'email' not in session:
         flash('Por gentileza, faça login!', 'danger')
         return redirect(url_for('login')) 
    produtos= Addproduto.query.all()     
    return render_template ('admin/index.html', title= 'Admnistração', produtos= produtos)


@app.route('/marcas')

def marcas():
    if 'email' not in session:
        flash('Por gentileza, faça login!', 'danger')
        return redirect(url_for('login'))
    marcas= Marcas.query.order_by(Marcas.id.desc()).all() 
    return render_template ('admin/marca.html', title= 'Fabricantes', marcas= marcas)    
        

@app.route('/categoria')

def categoria():
    if 'email' not in session:
        flash('Por gentileza, faça login!', 'danger')
        return redirect(url_for('login'))
    categorias= Categoria.query.order_by(Categoria.id.desc()).all() 
    return render_template ('admin/marca.html', title= 'Categoria', categorias= categorias) 



@app.route('/registrar', methods=['GET', 'POST'])

def registrar():
    form= RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password= bcrypt.generate_password_hash(form.password.data)
        user= User(name= form.name.data, username= form.username.data, email= form.email.data, password= hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Olá {form.name.data}, obrigado por se cadastrar!', 'success')
        return redirect(url_for('login'))
    return render_template('admin/registrar.html', form= form, title= 'Página de Cadastros')    



@app.route('/login', methods=['GET', 'POST']) 

def login():
   form= LoginFormulario(request.form)
   if request.method == 'POST' and form.validate():
       user= User.query.filter_by(email= form.email.data).first()
       if user and bcrypt.check_password_hash(user.password, form.password.data):
           session['email']= form.email.data
           flash(f'Olá {form.email.data}!', 'success')
           return redirect(request.args.get('next') or url_for('admin'))

       else:
             flash('Login inexistente, tente novamente!') 

   return render_template('admin/login.html', form=form, title= 'Login')    