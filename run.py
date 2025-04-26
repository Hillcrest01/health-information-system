from app import create_app, db
from app.commands import init_db
import click

app = create_app()

@app.cli.command("init-db")
def initialize_db():
    """Initialize the database"""
    init_db()
    print("Database initialized")

if __name__ == '__main__':
    app.run(debug=True)