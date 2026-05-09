from flask import Blueprint, render_template, redirect, request, url_for
from models import db, User
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user

auth_bp = Blueprint('auth', __name__)

bcrypt = Bcrypt()

@auth_bp.route('/')
def home():
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(
            request.form['password']
        ).decode('utf-8')

        user = User(username=username, password=password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(
            user.password,
            password
        ):
            login_user(user)
            return redirect(url_for('task.dashboard'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
