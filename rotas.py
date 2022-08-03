from crypt import methods
from xxlimited import foo
from flask import redirect, render_template, url_for, flash, request, session,current_app, make_response
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from loja import db, app, photos, bcrypt, login_manager
from .forms import CadastroClienteForm, ClienteLoginForm
import secrets, os
from .models import Cadastrar, ClientePedido
from flask_login import login_required, current_user, login_user, logout_user
import pdfkit
import stripe 

#chaves de pagmto stripe
publishable_key ='pk_test_51LQGJ5DhrUXYkCCGPdzauNxK8u49CEBbr7B4ImgvNtiWPI10DWIgSyxzzs3O8luxfPYsbGgG5qF26IexMjtbbDF700JqeI5d29'
stripe.api_key = 'sk_test_51LQGJ5DhrUXYkCCGu0xbJwZhE7525n4RGyeOVNzlcMdIy50vNO0PNnSoj9KbXfUry4udrIisGDdl3pz6c9TIxum600w5HAzhUq'

@app.route('/pagamento', methods=['POST'])
@login_required

def pagamento():

    notafiscal = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
    email=request.form['stripeEmail'],
    source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
    customer=customer.id,
    description='Fks shop',
    amount=amount,
    currency='brl',
    )
    cliente_pedido= ClientePedido.query.filter_by(cliente_id= current_user.id, notafiscal= notafiscal).order_by(ClientePedido.id.desc()).first()
    cliente_pedido.status= 'Pago'
    db.session.commit()
    return redirect(url_for('sucesso'))


@app.route('/sucesso')
def sucesso():
    return render_template('cliente/sucesso.html')


@app.route('/cliente/cadastrar', methods=['GET', 'POST'])

def cadastrar_clientes():
    form= CadastroClienteForm()
    if form.validate_on_submit():
        hash_password= bcrypt.generate_password_hash(form.password.data)
        cadastrar= Cadastrar(name= form.name.data, username= form.username.data,
        rg= form.rg.data, cpf= form.cpf.data, email= form.email.data,
        password= hash_password, country= form.country.data, city= form.city.data, address= form.address.data,
        district= form.district.data, contact= form.contact.data, zipcode= form.zipcode.data, state= form.state.data, birth= form.birth.data)
        db.session.add(cadastrar)
        flash(f'Obrigado {form.name.data} por se cadastrar', 'success')
        db.session.commit()
        return redirect(url_for('clienteLogin'))
    return render_template('cliente/cliente.html', form=form)


@app.route('/cliente/login', methods=['GET', 'POST'])

def clienteLogin():
    form= ClienteLoginForm()
    if form.validate_on_submit():
        user= Cadastrar.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next= request.args.get('next')
            flash('Login executado com sucesso, boas compras!', 'success')
            return redirect(next or url_for('home'))
        flash('Login inexistente, cheque seu email e senha!', 'danger')
        return redirect(url_for('clienteLogin'))
    return render_template('cliente/login.html', form=form)


@app.route('/cliente/logout')

def cliente_Logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/perfil')
 
def get_perfil():
    if current_user.is_authenticated:
        perfil = Cadastrar.query.get_or_404(current_user.id) 
        return render_template('/cliente/perfil.html', perfil= perfil )     
    return redirect('cliente/login')


@app.route('/updateperfil', methods=['GET', 'POST'])
 
def updateperfil():
    if current_user.is_authenticated:
        user= Cadastrar.query.get_or_404(current_user.id)
        form= CadastroClienteForm(request.form)

        if request.method == 'POST':
            user.name= form.name.data
            user.username= form.username.data
            user.email= form.email.data 
            user.country= form.country.data
            user.city= form.city.data       
            user.contact= form.contact.data
            user.address= form.address.data
            user.district= form.district.data
            user.state= form.state.data
            user.zipcode= form.zipcode.data
            user.profile= form.profile.data 
            db.session.commit()       
            flash('Produto foi atualizado com sucesso!', 'success')
            
            return redirect('/perfil')

        form.name.data= user.name
        form.username.data= user.username
        form.email.data= user.email
        form.contact.data= user.contact
        form.address.data= user.address
        form.district.data= user.district
        return render_template('/cliente/updateperfil.html', title= 'Atualizar Perfil', user= user, form= form )



def atualizarlojaCarro():
    for _key, user in session['LojainCarrinho'].items():
        session.modified= True
        del user['image']
        del user['colors']

    return atualizarlojaCarro 


@app.route('/pedido')
@login_required

def pedido():
    if current_user.is_authenticated:
        cliente_id= current_user.id
        notafiscal= secrets.token_hex(5)
        atualizarlojaCarro()
        
        try:
            p_order = ClientePedido(notafiscal = notafiscal, cliente_id = cliente_id, pedido = session['LojainCarrinho'])
            db.session.add(p_order)
            db.session.commit()
            session.pop('LojainCarrinho')
            flash('Seu pedido esta sendo processado!', 'success')
            return redirect(url_for('pedidos', notafiscal=notafiscal))

        except Exception as e:
            print(e)
            flash('Não foi possível processar seu pedido', 'danger')
            return redirect(url_for('getCart'))



@app.route('/pedidos/<notafiscal>')
@login_required

def pedidos(notafiscal):
    if current_user.is_authenticated:
        gtotal= 0
        subtotal= 0
        cliente_id= current_user.id
        cliente= Cadastrar.query.filter_by(id= cliente_id).first()
        pedidos= ClientePedido.query.filter_by(cliente_id= cliente_id, notafiscal= notafiscal).order_by(ClientePedido.id.desc()).first()
        for _key, user in pedidos.pedido.items():
            desconto = (user['discount']/100) * float(user['price'])
            subtotal += float(user['price']) * int(user['quantity'])
            subtotal -= desconto
            #imposto = ('%.2f' %(.06 * float(subtotal))) #1.06 valor aleatório de imposto
            gtotal = float('%.2f' %(subtotal))

    else:
            return redirect(url_for('clienteLogin'))    
    return render_template('cliente/pedido.html', notafiscal=notafiscal,  subtotal=subtotal, gtotal=gtotal,cliente=cliente, pedidos=pedidos )


@app.route('/get_pdf/<notafiscal>', methods=['POST'])
@login_required

def get_pdf(notafiscal):
    if current_user.is_authenticated:
        gtotal= 0 
        subtotal= 0
        cliente_id= current_user.id
        if request.method == 'POST':
            cliente= Cadastrar.query.filter_by(id= cliente_id).first()
            pedidos= ClientePedido.query.filter_by(cliente_id= cliente_id, notafiscal= notafiscal).order_by(ClientePedido.id.desc()).first()
            for _key, user in pedidos.pedido.items():
                desconto = (user['discount']/100) * float(user['price'])
                subtotal += float(user['price']) * int(user['quantity'])
                subtotal -= desconto
               # imposto = ('%.2f' %(.06 * float(subtotal))) #1.06 valor aleatório de imposto
                gtotal = float('%.2f'%(subtotal))
            rendered= render_template('cliente/pdf.html', notafiscal=notafiscal, subtotal=subtotal, gtotal=gtotal,cliente=cliente, pedidos=pedidos )
            pdf= pdfkit.from_string(rendered)
            response= make_response(pdf)
            response.headers['content-Type']='application/pdf' 
            response.headers['content-Disposition']='attched;filename' + notafiscal + '.pdf'
            return response
        return redirect(url_for('pedidos'))     


