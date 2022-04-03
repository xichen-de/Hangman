from sqlalchemy import MetaData, Column, types
from sqlalchemy.orm import declarative_base

meta = MetaData()
base_games = declarative_base(metadata=meta)


class Usage(base_games):
    __tablename__ = 'usage'
    usage_id = Column(types.Integer, primary_key=True)
    language = Column(types.Enum("en", "de", name="language_codes"), nullable=False)
    secret_word = Column(types.String(length=25), nullable=False)
    usage = Column(types.String(length=500), nullable=False)
    source = Column(types.String(length=100))
