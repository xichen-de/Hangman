import datetime
import uuid

from flask import Flask, g
from flask_cors import CORS
from flask_restx import Namespace, Resource, Api
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from server.hangman_orm import Usage, User, Game
from server.util import get_config

games_api = Namespace('games', description='Creating and playing games')
app = Flask(__name__)


@games_api.route('')
class Games(Resource):
    def post(self):
        # check input is valid
        if not (games_api.payload and
                'username' in games_api.payload and
                'language' in games_api.payload):
            games_api.abort(400, 'New game POST requires username and language')
        lang = games_api.payload['language']
        name = games_api.payload['username']
        user_id = str(uuid.uuid3(uuid.NAMESPACE_URL, name))
        if lang not in self.valid_langs:
            return {'message': 'New game POST language must be from ' +
                               ', '.join(Games.valid_langs)}, 400

        # if user does not exist, create user; get user id
        user = g.games_db.query(User).filter(User.user_id == user_id).one_or_none()
        if user is None:
            user = User(
                user_id=user_id,
                user_name=name,
                first_time=datetime.datetime.now(),
            )
            g.games_db.add(user)
            g.games_db.commit()
            user = g.games_db.query(User).filter(User.user_name == name).one()
        user._game_started(lang)

        # select a usage example
        usage = g.usage_db.query(Usage).filter(
            Usage.language == lang
        ).order_by(func.random()).first()

        # create the new game
        new_game_id = str(uuid.uuid4())
        new_game = Game(
            game_id=new_game_id,
            player=user.user_id,
            usage_id=usage.usage_id,
            bad_guesses=0,
            reveal_word='_' * len(usage.secret_word),
            start_time=datetime.datetime.now()
        )
        g.games_db.add(new_game)
        g.games_db.commit()

        return {'message': 'success', 'game_id': new_game_id}


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
