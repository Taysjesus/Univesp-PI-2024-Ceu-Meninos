from usuarios import database, app
from usuarios.models import Usuario
with app.app_context():
    database.drop_all()
    database.create_all()