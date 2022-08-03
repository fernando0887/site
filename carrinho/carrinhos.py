from unicodedata import name
from flask import redirect, render_template, url_for, flash, request, session,current_app
from loja import db, app
from loja.produtos.models import Addproduto
from loja.produtos.rotas import marcas, categorias
import json


def M_Dicionario(dic1,dic2):
    if isinstance(dic1, list) and isinstance(dic2, list):
        return dic1 + dic2

    elif isinstance(dic1, dict) and isinstance(dic2, dict):
        return dict(list(dic1.items()) + list(dic2.items()))
    return False

    


@app.route('/addCart', methods=['POST'])

def AddCart():
    try:
        produto_id = request.form.get('produto_id')
        quantity = int(request.form.get('quantity'))
        colors = request.form.get('colors')
        produto = Addproduto.query.filter_by(id= produto_id).first()

        if produto_id and quantity and colors and request.method == "POST":
            DicItems = {produto_id:{'name': produto.name, 'price':float(produto.price), 'discount': produto.discount,
            'quantity':quantity, 'colors': produto.colors, 'image': produto.image_1, 'color':colors}}

            if 'LojainCarrinho' in session:
                print(session['LojainCarrinho'])

                if produto_id in session['LojainCarrinho']:
                    if produto_id in session['LojainCarrinho']:
                        for key, item in session['LojainCarrinho'].items():
                            if int(key) == int(produto_id):
                                session.modified = True
                                item['quantity'] += 1
                   

                else:
                    session['LojainCarrinho'] = M_Dicionario(session['LojainCarrinho'], DicItems)
                    return redirect(request.referrer)

            else:
                session['LojainCarrinho'] = DicItems
                return redirect(request.referrer)

        
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)



@app.route('/carrinho')

def getCart():
    if 'LojainCarrinho' not in session:
        return redirect(request.referrer)
    subtotal= 0
    valorpagar= 0
    for key, produto in session['LojainCarrinho'].items():
        discount = (produto['discount']/100) * float(produto['price'])
        subtotal += float(produto['price']) * int(produto['quantity'])
        subtotal -= discount
        #imposto = ('%.2f'% (.06 * float(subtotal)))
        valorpagar = float('%.2f' %( subtotal))
    return render_template('produtos/carrinho.html',  valorpagar=valorpagar, marcas= marcas(), categorias= categorias()) #imposto= imposto   



@app.route('/updateCarrinho/<int:code>', methods= ['POST'])

def updateCarrinho(code):
    if 'LojainCarrinho' not in session and len(session['LojainCarrinho']) <= 0:
        return redirect(url_for('home'))

    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('colors')

        try:
            session.modified = True
            for key, item in session['LojainCarrinho'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['colors'] = color
                    flash('Produto atualizado com sucesso!', 'success')
                    return redirect(url_for('getCart'))
                    

        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))    



@app.route('/deleteitem/<int:id>')

def deleteitem(id):
    if 'LojainCarrinho' not in session and len(session['LojainCarrinho']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['LojainCarrinho'].items():
                if int(key) == id:
                    session['LojainCarrinho'].pop(key, None)
                    flash('Produto deletado com sucesso!', 'success')
                    return redirect(url_for('getCart'))
                    

    except Exception as e:
            print(e)
            return redirect(url_for('getCart')) 


@app.route('/esvaziarcarrinho')

def esvaziarcarrinho():
    try:
        session.pop('LojainCarrinho', None)
        return redirect(url_for('home'))
                    

    except Exception as e:
            print(e)
            return redirect(url_for('home'))                     