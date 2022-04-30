from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
