from app import create_app

app = create_app()

if __name__ == '__main__':
    # This allows running the app directly with `python autoapp.py`
    # which can be useful for some development scenarios,
    # though `flask run` is generally preferred for development.
    app.run(debug=True)
