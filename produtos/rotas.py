from flask import redirect, render_template, url_for, flash, request, session,current_app
from loja import db, app, photos
from loja.admin.rotas import categoria, marcas
from .models import Marcas, Categoria, Addproduto
from .forms import Addprodutos
import secrets, os


def marcas():
     marcas= Marcas.query.join(Addproduto, (Marcas.id == Addproduto.marca_id)).all()
     return marcas


def categorias():
     categorias= Categoria.query.join(Addproduto, (Categoria.id == Addproduto.categoria_id)).all()  
     return categorias


@app.route('/')

def home():
    pagina= request.args.get('pagina', 1, type= int)
    produtos= Addproduto.query.filter(Addproduto.stock > 0 ).order_by(Addproduto.id.desc()).paginate(page=pagina, per_page=5)    
    return render_template('produtos/index.html', produtos= produtos, marcas= marcas(), categorias= categorias()) 


@app.route('/search', methods=['GET', 'POST'])

def search():
    if request.method == 'POST':
        form= request.form
        search_value = form['search_string']
        search= '%{0}%'.format(search_value)
        produtos= Addproduto.query.filter(Addproduto.name.like(search)).all()
        return render_template('pesquisar.html', produtos= produtos, marcas= marcas(), categorias= categorias())
    else:
        return redirect('/')    
   

    

@app.route('/marca/<int:id>')
 
def get_marca(id):
    get_m = Marcas.query.filter_by(id=id).first_or_404()
    pagina= request.args.get('pagina', 1, type= int)
    marca= Addproduto.query.filter_by(marca= get_m).paginate(page=pagina, per_page=10)       
    return render_template('/produtos/index.html', marca= marca, marcas= marcas(), categorias= categorias(), get_m= get_m )    


@app.route('/produto/<int:id>')
 
def pagina_unica(id):
    produto = Addproduto.query.get_or_404(id)           
    return render_template('/produtos/pagina_unica.html', produto= produto, marcas= marcas(), categorias= categorias())    


@app.route('/categoria/<int:id>')
 
def get_categoria(id):
    pagina= request.args.get('pagina', 1, type= int)
    get_cat = Categoria.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduto.query.filter_by(categoria = get_cat).paginate(page=pagina, per_page=10)     
    return render_template('/produtos/index.html', get_cat_prod= get_cat_prod, categorias= categorias(), marcas= marcas(), get_cat= get_cat)    



@app.route('/addmarca', methods=['GET', 'POST'])

def addmarca():
    if 'email' not in session:
        flash('Por gentileza, faça login!', 'danger')
        return redirect(url_for('login')) 

    if request.method == 'POST':
        getmarca = request.form.get('marca')
        marca = Marcas(name=getmarca)
        db.session.add(marca)
        db.session.commit()
        flash(f'Marca {getmarca} cadastrada com sucesso!', 'success')
        return redirect(url_for('addmarca'))
    return render_template('/produtos/addmarca.html', marcas='marcas')


@app.route('/updatemarca/<int:id>', methods=['GET', 'POST'])
 
def updatemarca(id):
    if 'email' not in session:
        flash('Por gentileza, faça login!', 'danger')
        return redirect(url_for('login')) 

    updatemarca= Marcas.query.get_or_404(id)
    marca= request.form.get('marca')
    if request.method=='POST'   :
        updatemarca.name = marca
        flash(f'Fabricante atualizado com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('marcas'))         
    return render_template('/produtos/updatemarca.html', title= 'Atualizar Fabricantes', updatemarca= updatemarca )


@app.route('/deletemarca/<int:id>', methods=['POST'])

def deletemarca(id): 

    marca= Marcas.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(marca)
        db.session.commit()
        flash(f'Fabricante {marca.name} apagado com sucesso!', 'success')
        return redirect(url_for('admin'))         
    
    flash(f'Fabricante {marca.name} não foi apagado!', 'warning')
    return redirect(url_for('admin'))     


@app.route('/addcat', methods=['GET', 'POST'])

def addcat():
    if 'email' not in session:
        flash('Por gentileza, faça login!', 'danger')
        return redirect(url_for('login')) 

    if request.method == 'POST':
        getmarca = request.form.get('categoria')
        cat = Categoria(name=getmarca)
        db.session.add(cat)
        db.session.commit()
        flash(f'Categoria {getmarca} cadastrada com sucesso!', 'success')
        return redirect(url_for('addcat'))
    return render_template('/produtos/addmarca.html')


@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
 
def updatecategoria(id):
    if 'email' not in session:
        flash('Por gentileza, faça login!', 'danger')
        return redirect(url_for('login')) 

    updatecategoria= Categoria.query.get_or_404(id)
    categoria= request.form.get('categoria')
    if request.method=='POST'   :
        updatecategoria.name = categoria
        flash(f'Categoria atualizada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('categoria'))         
    return render_template('/produtos/updatecategoria.html', title= 'Atualizar Categoria', updatecategoria= updatecategoria )



@app.route('/deletecategoria/<int:id>', methods=['POST'])

def deletecategoria(id): 
    categoria= Categoria.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(categoria)
        db.session.commit()
        flash(f'Categoria {categoria.name} apagado com sucesso!', 'success')
        return redirect(url_for('admin'))         
    
    flash(f'Fabricante {categoria.name} não foi apagado!', 'warning')
    return redirect(url_for('admin'))     



@app.route('/addproduto', methods=['GET', 'POST'])

def addproduto():
    if 'email' not in session:
         flash('Por gentileza, faça login!', 'danger')
         return redirect(url_for('login')) 

    marcas= Marcas.query.all()
    categorias= Categoria.query.all()
    form= Addprodutos(request.form)
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc= form.discription.data
        marca= request.form.get('marca')
        categoria= request.form.get('categoria')
        image_1= photos.save(request.files.get('img_1'), name=secrets.token_hex(20) + '.')
        image_2= photos.save(request.files.get('img_2'), name=secrets.token_hex(20) + '.')
        image_3= photos.save(request.files.get('img_3'), name=secrets.token_hex(20) + '.')
        addpro= Addproduto(name= name, price= price, discount= discount, stock= stock, colors= colors, desc= desc, marca_id= marca, categoria_id= categoria,
        image_1= image_1, image_2= image_2, image_3= image_3)
        db.session.add(addpro)    
        flash(f'Produto {name} cadastrado com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('/produtos/addproduto.html', title= 'Cadastrar Produtos', form= form, marcas= marcas, categorias= categorias)


@app.route('/updateproduto/<int:id>', methods=['GET', 'POST'])
 
def updateproduto(id):
    marcas= Marcas.query.all()
    categorias= Categoria.query.all()
    produto= Addproduto.query.get_or_404(id)
    marca= request.form.get('marca')
    categoria= request.form.get('categoria')
    form= Addprodutos(request.form)

    if request.method == 'POST':
        produto.name= form.name.data
        produto.price= form.price.data
        produto.discount= form.discount.data 
        produto.marca_id= marca
        produto.categoria_id= categoria       
        produto.stock= form.stock.data
        produto.colors= form.colors.data
        produto.desc= form.discription.data

        if request.files.get('img_1'):
            try:

                 os.unlink(os.path.join(current_app.root_path, 'static/images/' + produto.image_1))
                 produto.image_1= photos.save(request.files.get('img_1'), name=secrets.token_hex(20) + '.')

            except:
                produto.image_1= photos.save(request.files.get('img_1'), name=secrets.token_hex(20) + '.')


        if request.files.get('img_2'):
            try:

                 os.unlink(os.path.join(current_app.root_path, 'static/images/' + produto.image_2))
                 produto.image_2= photos.save(request.files.get('img_2'), name=secrets.token_hex(20) + '.')

            except:
                produto.image_2= photos.save(request.files.get('img_2'), name=secrets.token_hex(20) + '.')

        
        if request.files.get('img_3'):
            try:

                 os.unlink(os.path.join(current_app.root_path, 'static/images/' + produto.image_3))
                 produto.image_3= photos.save(request.files.get('img_3'), name=secrets.token_hex(20) + '.')

            except:
                produto.image_3= photos.save(request.files.get('img_3'), name=secrets.token_hex(20) + '.')


        db.session.commit()       
        flash('Produto foi atualizado com sucesso!', 'success')
        
        return redirect('/admin')

    form.name.data= produto.name
    form.price.data= produto.price
    form.discription.data= produto.desc
    form.stock.data= produto.stock
    form.colors.data= produto.colors
    form.discount.data= produto.discount
    return render_template('/produtos/updateproduto.html', title= 'Atualizar Produtos', marcas= marcas, categorias= categorias, produto= produto, form= form )


@app.route('/deleteproduto/<int:id>', methods=['GET','POST'])

def deleteproduto(id): 
    produto= Addproduto.query.get_or_404(id)
    if request.method=='POST':
        
        if request.files.get('img_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, '/static/images/' + produto.image_1))
                produto.image_1= photos.delete(request.files.get('img_1'))
                os.unlink(os.path.join(current_app.root_path, '/static/images/' + produto.image_2))
                produto.image_2= photos.delete(request.files.get('img_2'))
                os.unlink(os.path.join(current_app.root_path, '/static/images/' + produto.image_3))
                produto.image_3= photos.delete(request.files.get('img_3'))

            except Exception as e:
                print(e)

        db.session.delete(produto)    
        db.session.commit()
        flash(f'Produto {produto.name} deletado com sucesso!', 'success')
        return redirect(url_for('admin'))   
    
    return redirect(url_for('admin'))   