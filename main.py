from flask import Flask, Response, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json
import jinja2
from werkzeug.utils import redirect

app = Flask(__name__)



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://murillojulio:bXVyaWxsb2p1@jobs.visie.com.br/murillojulio'

db = SQLAlchemy(app)

class Pessoas(db.Model):
    id = db.Column('id_pessoa', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    rg = db.Column(db.String(100))
    cpf = db.Column(db.String(100))
    data_nascimento = db.Column(db.Date)
    data_admissao = db.Column(db.Date)
    funcao = db.Column(db.String(100))

    def __init__(self, nome, rg, cpf, data_nascimento, data_admissao):
        self.nome = nome
        self.rg = rg
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.data_admissao = data_admissao


# select all
app.route("/pessoas", methods=["GET"])
def seleciona_usuarios():
    pessoa = Pessoas.query.all
    print(pessoa)
    return Response()

# select one

# cadsatrar

# atualizar

# deletar

@app.route("/")
def index():
    pessoas = Pessoas.query.all()
    return render_template('Index.html', pessoas=pessoas)



@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        pessoa = Pessoas(request.form['nome'], request.form['rg'], request.form['cpf'], request.form['data_nascimento'], request.form['data_admissao'])
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
    db.create_all()
    app.run()
