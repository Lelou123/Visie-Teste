from flask import Flask, Response, request, render_template, url_for
from werkzeug.utils import redirect
from src.models import db, Pessoas
import mysql.connector
import json
import jinja2

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://murillojulio:bXVyaWxsb2p1@jobs.visie.com.br/murillojulio'


@app.route("/", methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pessoas = Pessoas.query.paginate(page=page, per_page=8)
    if request.method == 'POST':
        if request.form.get('action') == 'Ver Paginado':
            pessoas = Pessoas.query.paginate(page=page, per_page=8)
        elif request.form.get('action1') == 'Admissao(Decres)':
            pessoas = Pessoas.query.order_by(Pessoas.data_admissao.desc()).paginate(page=page, per_page=100)
        elif request.form.get('action2') == 'Admissao(Cresc)':
            pessoas = Pessoas.query.order_by(Pessoas.data_admissao).paginate(page=page, per_page=100)
        elif request.form.get('action3') == 'Alfabetica(Decres)':
            pessoas = Pessoas.query.order_by(Pessoas.nome.desc()).paginate(page=page, per_page=100)
        elif request.form.get('action4') == 'Alfabetica(Cresc)':
            pessoas = Pessoas.query.order_by(Pessoas.nome).paginate(page=page, per_page=100)
        else:
            pass

    for item in pessoas.items:
        item.nome = item.nome.split(' ')[0]

    return render_template('index.html', pessoas=pessoas)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        pessoa = Pessoas(request.form['nome'], request.form['rg'], request.form['cpf'], request.form['data_nascimento'],
                         request.form['data_admissao'])
        db.session.add(pessoa)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    pessoa = Pessoas.query.get(id)
    if request.method == 'POST':
        pessoa.nome = request.form['nome']
        pessoa.rg = request.form['rg']
        pessoa.cpf = request.form['cpf']
        pessoa.data_nascimento = request.form['data_nascimento']
        pessoa.data_admissao = request.form['data_admissao']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', pessoa=pessoa)


@app.route('/delete/<int:id_pessoa>')
def delete(id_pessoa):
    pessoa = Pessoas.query.get(id_pessoa)
    db.session.delete(pessoa)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    db.init_app(app=app)
    with app.test_request_context():
        db.create_all()
    app.run()
