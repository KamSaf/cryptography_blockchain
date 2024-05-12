from src.routes.api import API_ROUTES_BP
from src.routes.gui import GUI_ROUTES_BP


def init_app(app):
    app.register_blueprint(API_ROUTES_BP)
    app.register_blueprint(GUI_ROUTES_BP)
