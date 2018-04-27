from app.controllers.BaseController import BaseController
from app.models.Users import User
from app import db
from flask import flash, make_response, redirect, render_template, url_for
from flask_login import login_user, logout_user, current_user

import hashlib

users = { 'joe': 'abc123' }
LOGIN_ERROR = 'Your username or password did not match our records. Please try again.'

class LoginController(BaseController):

    def __init__(self):
        super().__init__()

    def login(self, request):
        if request.method == 'GET':
            if current_user.is_authenticated:
                return redirect(url_for('index'))
            return make_response(render_template('login.html'))

        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()
        user = User.query.filter_by(username=username).first()
             
        if user:
            if password == user.password:
                login_user(user)
            else: #passwords do not match
                return make_response(render_template('login.html', error=LOGIN_ERROR))

        else: #user does not exist, create new
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
        
        return redirect(url_for('index'))

    def logout(self, request):
        logout_user()
        return redirect(url_for('index'))