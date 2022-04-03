import os

from flask import Flask
from sqlalchemy import create_engine

from server.hangman_orm import base_games
from server.util import get_config

app = Flask(__name__)


@app.cli.command("init-db")
def init_db():
    config = get_config(os.environ["FLASK_ENV"], open("server/config.yaml"))
    print("Initializing database...")
    db = create_engine(config["database"])
    base_games.metadata.create_all(db)
    print("Database initialized.")
