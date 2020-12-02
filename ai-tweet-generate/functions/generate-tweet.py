import json
from libs import gpt
from libs import handler
from libs import twitter


def generate_tweet(event):
    body = json.loads(event['body'])
    username = twitter.strip_username(body['username'])
    tweets = twitter.get_tweets(username)
    prediction = gpt.make_prediction(username, tweets)
    return {
        "tweet": prediction,
        "username": username
    }


def post(event, context):
    payload, status = handler.wrap_function(generate_tweet, event, 201)

    return {
        'statusCode': status,
        'headers': handler.get_headers('POST'),
        'body': json.dumps(payload)
    }
