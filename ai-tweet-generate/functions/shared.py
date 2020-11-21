import json
from libs import handler
from libs.db import tweets_db


def post_shared(event):
    body = json.loads(event['body'])
    tweet_id = tweets_db.insert_tweet({
        'tweet': body['tweet'],
        'username': body['username'],
        'views': 0
    })
    return {
        'tweetId': tweet_id
    }


# Don't return everything from database, just these keys
return_keys = ['tweet', 'username']


def get_shared(event):
    tweet_id = event['pathParameters']['tweetId']
    tweet = tweets_db.get_tweet(tweet_id)
    return handler.serialize(tweet.items(), return_keys)


def get(event, context):
    payload, status = handler.wrap_function(get_shared, event)

    return {
        'statusCode': status,
        'headers': handler.get_headers(),
        'body': json.dumps(payload, default=str)
    }


def post(event, context):
    payload, status = handler.wrap_function(post_shared, event, 201)

    return {
        'statusCode': status,
        'headers': handler.get_headers(),
        'body': json.dumps(payload)
    }
