import datetime
import json

from sqlalchemy import MetaData, Column, types
from sqlalchemy.orm import declarative_base

from server.util import date_to_ordinal

meta = MetaData()
base_games = declarative_base(meta)
base_usage = declarative_base(meta)


class Usage(base_usage):
    __tablename__ = 'usages'
    usage_id = Column(types.Integer, primary_key=True)
    language = Column(types.Enum("en", "es", "fr", name='language_codes'), nullable=False)
    secret_word = Column(types.String(length=25), nullable=False)
    usage = Column(types.String(length=400), nullable=False)
    source = Column(types.String(length=100))


class User(base_games):
    __tablename__ = 'users'
    user_id = Column(types.String(length=38), primary_key=True)
    user_name = Column(types.String(length=30), nullable=False)
    num_games = Column(types.Integer, default=0)
    outcomes = Column(types.Text, default='{}')
    by_lang = Column(types.Text, default='{}')
    first_time = Column(types.DateTime)
    total_time = Column(types.Interval)
    avg_time = Column(types.Interval)

    def _incr_json_field(self, field, key):
        d = json.loads(getattr(self, field))
        d[key] = d.get(key, 0) + 1
        setattr(self, field, json.dumps(d))

    def _decr_json_field(self, field, key):
        d = json.loads(getattr(self, field))
        d[key] = d.get(key, 0) - 1
        setattr(self, field, json.dumps(d))

    def _game_started(self, lang):
        self.num_games = (self.num_games or 0) + 1
        self._incr_json_field('outcomes', 'active')
        self._incr_json_field('by_lang', lang)

    def _game_ended(self, outcome, time_delta):
        self._decr_json_field('outcomes', 'active')
        self._incr_json_field('outcomes', outcome)
        self.total_time = time_delta + (self.total_time or datetime.timedelta(0))
        self.avg_time = self.total_time / self.num_games


class Game(base_games):
    __tablename__ = 'games'
    game_id = Column(types.String(length=38), primary_key=True)
    player = Column(types.String(length=38), nullable=False)
    usage_id = Column(types.Integer, nullable=False)
    guessed = Column(types.String(length=30), default='')
    reveal_word = Column(types.String(length=25), nullable=False)
    bad_guesses = Column(types.Integer)
    start_time = Column(types.DateTime)
    end_time = Column(types.DateTime)

    def _result(self):
        if self.bad_guesses == 6:
            return 'lost'
        elif '_' not in self.reveal_word:
            return 'won'
        else:
            return 'active'

    def _to_dict(self):
        as_dict = {k: v for k, v in self.__dict__.items()
                   if not k.startswith('_')}
        as_dict['result'] = self._result()
        as_dict['start_time'] = date_to_ordinal(as_dict.get('start_time'))
        as_dict['end_time'] = date_to_ordinal(as_dict.get('end_time'))
        return as_dict
