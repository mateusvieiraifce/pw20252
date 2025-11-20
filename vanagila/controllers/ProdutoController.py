from flask import Flask, render_template, request, redirect, url_for
from models import Produtos
from main import app, session

@app.route('/produto', methods=['GET'])
def get_produtos():
    produtos = session.query(Produtos).all()
    return render_template('produtos/list_produto.html', produtos=produtos)

@app.route('/produto/create', methods=['GET'])
def create_produto():
    return render_template('produtos/create_produto.html')

@app.route('/produto/create', methods=['POST'])
def create_produto_do():
    codigo = request.form['codigo']
    descricao = request.form['descricao']
    preco = request.form['preco']
    estoque = request.form['estoque']

    new_produto = Produtos(codigo=codigo, descricao=descricao, preco=preco, estoque=estoque)
    session.add(new_produto)
    session.commit()
    
    return redirect(url_for('get_produtos'))

@app.route('/produto/delete/<int:id>', methods=['GET'])
def delete_produto(id):
    produto = session.query(Produtos).filter_by(id=id).first()
    msg = 'Produto deletado com sucesso'
    if not produto:
        msg = 'Produto não encontrado'
        return redirect(url_for('create_produto', mesg=msg))
    try:
        session.delete(produto)
        session.commit()
    except:
        msg = 'Erro ao deletar produto'
        session.rollback()
    return redirect(url_for('get_produtos', msg=msg))

@app.route('/produto/search', methods=['POST'])
def search_produto():
    codigo = request.form['codigo']
    descricao = request.form['descricao']

    produtos = session.query(Produtos).filter(Produtos.codigo.contains(codigo), Produtos.descricao.contains(descricao)).all()

    return render_template('produtos/list_produto.html', produtos=produtos)

@app.route('/produto/edit/<int:id>', methods=['GET'])
def edit_produto(id):
    produto = session.query(Produtos).filter_by(id=id).first()
    if not produto:
        msg = 'Produto não encontrado'
        return redirect(url_for('get_produto', mesg=msg))
    
    return render_template('produtos/edit_produto.html', produto=produto)

@app.route('/produto/edit/<int:id>', methods=['POST'])
def edit_produto_do(id):
    produto = session.query(Produtos).filter_by(id=id).first()
    if not produto:
        msg = 'Produto não encontrado'
        return redirect(url_for('get_produto', mesg=msg))
    
    try:
        produto.codigo = request.form['codigo']
        produto.descricao = request.form['descricao']
        produto.preco = request.form['preco']
        produto.estoque = request.form['estoque']

        session.commit()
        msg = 'Produto atualizado com sucesso!'
    except:
        session.rollback()
        msg = 'Erro ao atualizar produto.'
    
    return redirect(url_for('get_produtos', msg=msg))