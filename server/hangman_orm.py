from sqlalchemy import MetaData, Column, types, ForeignKey
from sqlalchemy.orm import declarative_base

meta = MetaData()
base_games = declarative_base(metadata=meta)
base_usage = declarative_base(metadata=meta)


class Usage(base_usage):
    __tablename__ = 'usage'
    usage_id = Column(types.Integer, primary_key=True)
    language = Column(types.Enum("en", "es", "fr", name='language_codes'), nullable=False)
    secret_word = Column(types.String(length=25), nullable=False)
    usage = Column(types.String(length=500), nullable=False)
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


class Game(base_games):
    __tablename__ = 'games'
    game_id = Column(types.String(length=38), primary_key=True)
    player = Column(types.String(length=38), ForeignKey(User.user_id), nullable=False)
    usage_id = Column(types.Integer, nullable=False)
    guessed = Column(types.String(length=30), default='')
    reveal_word = Column(types.String(length=25), nullable=False)
    bad_guesses = Column(types.Integer)
    start_time = Column(types.DateTime)
    end_time = Column(types.DateTime)
