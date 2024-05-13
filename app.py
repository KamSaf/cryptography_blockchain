from src.config import app
from src import init_app
from datetime import datetime

init_app(app)
app.jinja_env.globals.update(
    to_datetime=datetime.fromtimestamp,
    date_format=datetime.strftime
)

if __name__ == '__main__':
    app.run(debug=True)
