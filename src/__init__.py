from .routes import routes_bp


def init_app(app):
    app.register_blueprint(routes_bp)
