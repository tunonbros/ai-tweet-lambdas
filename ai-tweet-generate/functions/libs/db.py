import os

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, Integer, DateTime
from sqlalchemy.sql import func, select, update

from short_url import UrlEncoder


class TweetsDB:
    def __init__(self, user=None, password=None, host=None, port=None, database=None):
        self.user = user or os.environ['DB_USER']
        self.password = password or os.environ['DB_PASSWORD']
        self.host = host or os.environ['DB_HOST']
        self.port = port or 5432
        self.database = database or 'aitweet'
        self.id_generator = UrlEncoder(alphabet='UsGHgtbu7PBxLq3KZpThmy2NSA8EC4MzJdcWXV6wanrkjefYRF5DQv9')

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
        # Let's fetch by id, instead of by tweet_id (just for fun)
        id_num = self.id_generator.decode_url(tweet_id)
        s = select([self.tweets]).where(self.tweets.c.id == id_num)

        # Update views count
        u = update(self.tweets, values={self.tweets.c.views: self.tweets.c.views + 1})
        self.conn.execute(u)

        # Return select result
        return self.conn.execute(s).fetchone()

    def insert_tweet(self, tweet):
        # Insert
        ins = self.tweets.insert().returning(self.tweets.c.id)
        res = self.conn.execute(ins, **tweet)
        id_num = res.fetchone()[self.tweets.c.id]

        # Calculate tweet_id
        return self.id_generator.encode_url(id_num)

        # TODO: Update
        # upd = self.tweets.update().where(self.tweets.c.id == id_num).values(tweet_id=tweet_id)


tweets_db = TweetsDB()
