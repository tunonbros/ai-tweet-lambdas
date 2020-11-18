import json
import os

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, Integer, DateTime
from sqlalchemy.sql import func


class DB:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

        db_string = "postgres://{}:{}@{}:{}/{}".format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.database
        )

        self.db = create_engine(db_string)

        self.meta = MetaData(self.db)

        self.user_table = Table(
            'tweets', self.meta,
            Column('id', Integer, primary_key=True),
            Column('tweet', String),
            Column('username', String),
            Column('views', Integer),
            Column('created_at', DateTime(timezone=True), server_default=func.now()),
            Column('updated_at', DateTime(timezone=True), onupdate=func.now())
        )

    def create_tables(self):
        self.meta.create_all(self.db)

        return True


def lambda_handler(event, context):
    db_instance = DB(
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        port=5432,
        database='aitweet'
    )

    db_instance.create_tables()

    return {
        'statusCode': 200,
        'body': json.dumps('All tables have been created')
    }
