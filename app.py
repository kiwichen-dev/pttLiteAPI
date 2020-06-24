from api import create_app

app = create_app()

from api.route import hotBoard,index,article,search

if __name__ == "__main__":
    app.run(debug=True)