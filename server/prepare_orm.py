import csv
import os

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.hangman_orm import base_usage, base_games, Usage
from server.util import get_config, get_project_root

app = Flask(__name__)


def init_db():
    print("Initializing database...")
    config = get_config(os.environ["FLASK_ENV"], open(os.path.join(get_project_root(), "server/config.yaml")))
    db_usage = create_engine(config['DB_USAGE'])
    base_usage.metadata.create_all(db_usage)
    db_games = create_engine(config['DB_GAMES'])
    base_games.metadata.create_all(db_games)
    session = sessionmaker(db_usage)()
    if session.query(Usage).count() == 0:
        data = []
        reader = csv.reader(open(os.path.join(get_project_root(), "data/usages.csv"), encoding='utf8'))
        for row in reader:
            if len(row[4]) <= 500:
                data.append(Usage(
                    usage_id=int(row[0]),
                    language=row[1],
                    secret_word=row[3],
                    usage=row[4],
                    source=row[5]
                ))

        print('Adding', len(data), 'rows to Usage table')
        session.add_all(data)
        session.commit()
    print("Database initialized.")


if __name__ == '__main__':
    init_db()
