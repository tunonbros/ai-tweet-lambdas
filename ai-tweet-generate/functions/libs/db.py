import os

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, Integer, DateTime
from sqlalchemy.sql import func, select


class TweetsDB:
    def __init__(self, user=None, password=None, host=None, port=None, database=None):
        self.user = user or os.environ['DB_USER']
        self.password = password or os.environ['DB_PASSWORD']
        self.host = host or os.environ['DB_HOST']
        self.port = port or 5432
        self.database = database or 'aitweet'

        db_string = "postgres://{}:{}@{}:{}/{}".format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.database
        )

        self.db = create_engine(db_string)
        self.meta = MetaData(self.db)

        self.tweets = Table(
            'tweets', self.meta,
            Column('id', Integer, primary_key=True),
            Column('tweet', String),
            Column('username', String),
            Column('views', Integer),
            Column('created_at', DateTime(timezone=True), server_default=func.now()),
            Column('updated_at', DateTime(timezone=True), onupdate=func.now()),
            Column('tweet_id', String(64)),
        )

        self.conn = self.db.connect()

    def create_tables(self):
        self.meta.create_all(self.db)
        return True

    def get_tweet(self, tweet_id):
        s = select([self.tweets]).where(self.tweets.c.tweet_id == tweet_id)
        return self.conn.execute(s).fetchone()

    def insert_tweet(self, tweet):
        ins = self.tweets.insert()
        self.conn.execute(ins, **tweet)


tweets_db = TweetsDB()
