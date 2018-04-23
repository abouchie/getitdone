from app.controllers.BaseController import BaseController
from flask import render_template

class HomeController(BaseController):

    def __init__(self):
        super().__init__()

    def index(self):
        return render_template('index.html')