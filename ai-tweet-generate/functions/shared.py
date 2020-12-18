import json
from libs import handler
from libs.db import tweets_db


def get_shared(event, params):
    tweet = tweets_db.get_tweet(params[0])

    # Don't return everything from database, just these keys
    return_keys = ['tweet', 'username']
    return handler.serialize(tweet.items(), return_keys)


def get(event, params):
    payload, status = handler.wrap_function(get_shared, event, params)

    return {
        'statusCode': status,
        'headers': handler.get_headers(),
        'body': json.dumps(payload, default=str)
    }
