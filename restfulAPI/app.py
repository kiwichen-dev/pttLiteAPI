from api import App

run = App()
app = run.create_app()

if __name__ == "__main__":
    app.run(debug=True)