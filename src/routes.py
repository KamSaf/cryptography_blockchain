from flask import Blueprint
from .config import app

routes_bp = Blueprint('routes', __name__)


@app.route('/')
def home_page():
    return {"message": "Hello!"}


@app.route('/about')
def about_page():
    return {"message": "Hello!"}
