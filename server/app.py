from flask import Flask, g
from flask_cors import CORS
from flask_restx import Namespace, Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.hangman_orm import Usage
from server.util import get_config

games_api = Namespace('games', description='Creating and playing games')
app = Flask(__name__)


@games_api.route('')
class Games(Resource):
    def post(self):
        """Create a new game and return the game id"""
        num_games = g.usage_db.query(Usage).count()
        return {'message': 'games POST under construction - ' + str(num_games) + ' games'}


@games_api.route('/<game_id>')
class OneGame(Resource):
    def get(self, game_id):
        """Get the state of the game"""
        return {'message': 'Game GET under construction'}

    def put(self, game_id):
        """Guess a letter and update the game state accordingly"""
        return {'message': 'Game PUT under construction'}

    def delete(self, game_id):
        """End the game, delete the record"""
        return {'message': 'Game DELETE under construction'}


@app.before_request
def init_db():
    """Initialize db by creating the global db_session"""
    if not hasattr(g, 'usage_db'):
        db_usage = create_engine(app.config['DB_USAGE'])
        g.usage_db = sessionmaker(db_usage)()

    if not hasattr(g, 'games_db'):
        db_games = create_engine(app.config['DB_GAMES'])
        g.games_db = sessionmaker(db_games)()


@app.teardown_request
def close_db(exception):
    """Close down db connection; same one cannot be used b/w threads"""
    if hasattr(g, 'usage_db'):
        g.usage_db.close()
        _ = g.pop('usage_db')

    if hasattr(g, 'games_db'):
        g.games_db.close()
        _ = g.pop('games_db')


if __name__ == '__main__':
    app.config.update(get_config(app.config['ENV'],
                                 app.open_resource('config.yaml')))
    CORS(app)  # Cross-origin resource sharing
    api = Api(app)
    api.add_namespace(games_api, path='/api/games')
    app.run(debug=True)
