from app.controllers.BaseController import BaseController
from app.models.Users import User
from app import db
from flask import flash, make_response, redirect, render_template, url_for
from flask_login import login_user, logout_user, current_user

users = { 'joe': 'abc123' }
LOGIN_ERROR = 'Your username or password did not match our records. Please try again.'

class LoginController(BaseController):

    def __init__(self):
        super().__init__()

    def login(self, request):
        if request.method == 'GET':
            if current_user.is_authenticated:
                return redirect(url_for('index'))
            print(current_user.is_authenticated)
            print(current_user)  
            return make_response(render_template('login.html'))

        username = request.form['username']
        if request.form['password'] == users[username]:
            
            user = User.query.filter_by(username=username).first()
            if not user:
                user = User(username)
                db.session.add(user)
                db.session.commit()

            login_user(user)
            
            return redirect(url_for('index'))
        return make_response(render_template('login.html', error=LOGIN_ERROR))

    def logout(self, request):
        logout_user()
        return redirect(url_for('index'))