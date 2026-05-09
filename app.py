from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User

from extensions import socketio

from routes.auth import auth_bp

# ================= APP =================

app = Flask(__name__)

app.config.from_object(Config)

# ================= DATABASE =================

db.init_app(app)

# ================= SOCKET =================

socketio.init_app(app)

# ================= LOGIN =================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


# ================= IMPORT ROUTES =================

from routes.task import task_bp

# ================= BLUEPRINTS =================

app.register_blueprint(auth_bp)

app.register_blueprint(task_bp)

# ================= CREATE TABLES =================

with app.app_context():

    db.create_all()

# ================= MAIN =================

if __name__ == '__main__':

    socketio.run(
        app,
        debug=True
    )