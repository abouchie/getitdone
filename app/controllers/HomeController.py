from app.controllers.BaseController import BaseController
from flask import render_template
from flask_login import current_user

class HomeController(BaseController):

    def __init__(self):
        super().__init__()

    def index(self):
        print('from home')
        print(current_user)
        return render_template('index.html')