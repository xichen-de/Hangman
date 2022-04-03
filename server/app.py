from flask import Flask
from flask_cors import CORS
from flask_restx import Namespace, Resource, Api

from server.util import get_config

games_api = Namespace('games', description='Creating and playing games')


@games_api.route('')
class Games(Resource):
    def post(self):
        """Create a new game and return the game id"""
        return {'message': 'Games POST under construction'}


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


if __name__ == '__main__':
    app = Flask(__name__)
    app.config.update(get_config(app.config['ENV'],
                                 app.open_resource('config.yaml')))
    CORS(app)  # Cross-origin resource sharing
    api = Api(app)
    api.add_namespace(games_api, path='/api/games')
    app.run(debug=True)
