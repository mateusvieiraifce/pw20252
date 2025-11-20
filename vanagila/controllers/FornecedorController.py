from flask import render_template, request, redirect, url_for
from models import Fornecedor
from main import app, session

@app.route('/fornecedor', methods=['GET'])
def get_fornecedores():
    fornecedores = session.query(Fornecedor).all()
    return render_template('fornecedores/list_fornecedor.html', fornecedores=fornecedores)

@app.route('/fornecedor/create', methods=['GET'])
def create_fornecedor():
    return render_template('fornecedores/create_fornecedor.html')

@app.route('/fornecedor/create', methods=['POST'])
def create_fornecedor_do():
    cnpj = request.form['cnpj']
    nome = request.form['nome']
    endereco = request.form['endereco']
    telefone = request.form['telefone']
    email = request.form['email']
    inscricao_estadual = request.form['inscricao_estadual']
    inscricao_municipal = request.form['inscricao_municipal']
    cep = request.form['cep']

    new_fornecedor = Fornecedor(cnpj=cnpj, nome=nome, endereco=endereco, telefone=telefone, email=email, inscricao_estadual=inscricao_estadual, inscricao_municipal=inscricao_municipal, cep=cep)
    session.add(new_fornecedor)
    session.commit()

    return redirect(url_for('get_fornecedores'))

@app.route('/fornecedor/delete/<int:id>', methods=['GET'])
def delete_fornecedor(id):
    fornecedor = session.query(Fornecedor).filter_by(id=id).first()
    msg = 'Fornecedor deletado com sucesso'
    if not fornecedor:
        msg = 'Fornecedor não encontrado'
        return redirect(url_for('get_fornecedores', mesg=msg))
    try:
        session.delete(fornecedor)
        session.commit()
    except:
        msg = 'Erro ao deletar fornecedor'
        session.rollback()
    return redirect(url_for('get_fornecedores', msg=msg))


@app.route('/fornecedor/search', methods=['POST'])
def search_fornecedor():
    cnpj = request.form['cnpj']
    nome = request.form['nome']

    fornecedores = session.query(Fornecedor).filter(Fornecedor.cnpj.contains(cnpj), Fornecedor.nome.contains(nome)).all()

    return render_template('fornecedores/list_fornecedor.html', fornecedores=fornecedores)

@app.route('/fornecedor/edit/<int:id>', methods=['GET'])
def edit_fornecedor(id):
    fornecedor = session.query(Fornecedor).filter_by(id=id).first()
    if not fornecedor:
        msg = 'Fornecedor não encontrado'
        return redirect(url_for('get_fornecedores', mesg=msg))
    
    return render_template('fornecedores/edit_fornecedor.html', fornecedor=fornecedor)

@app.route('/fornecedor/edit/<int:id>', methods=['POST'])
def edit_fornecedor_do(id):
    fornecedor = session.query(Fornecedor).filter_by(id=id).first()
    if not fornecedor:
        msg = 'Fornecedor não encontrado'
        return redirect(url_for('get_fornecedores', mesg=msg))
    
    try:
        fornecedor.cnpj = request.form['cnpj']
        fornecedor.nome = request.form['nome']
        fornecedor.endereco = request.form['endereco']
        fornecedor.telefone = request.form['telefone']
        fornecedor.email = request.form['email']
        fornecedor.inscricao_estadual = request.form['inscricao_estadual']
        fornecedor.inscricao_municipal = request.form['inscricao_municipal']

        session.commit()
        msg = 'Fornecedor atualizado com sucesso!'
    except:
        session.rollback()
        msg = 'Erro ao atualizar fornecedor.'
    
    return redirect(url_for('get_fornecedores', msg=msg))