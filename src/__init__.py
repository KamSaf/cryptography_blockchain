from .routes import API_ROUTES_BP


def init_app(app):
    app.register_blueprint(API_ROUTES_BP)
