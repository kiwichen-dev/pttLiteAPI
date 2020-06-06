from api import create_app
from api import pool

app = create_app()

if __name__ == "__main__":
    app.run()