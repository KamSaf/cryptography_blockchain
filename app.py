from src.config import app
from src import init_app

init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
