#Criando a extrutura do Banco de Dados
from usuarios import database, login_manager
from flask_login import UserMixin
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)


class Agendamento(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=False)
    date = database.Column(database.String(10), nullable=False)
    time = database.Column(database.String(5), nullable=False)

