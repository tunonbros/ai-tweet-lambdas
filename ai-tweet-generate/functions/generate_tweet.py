import json
from libs import gpt
from libs import handler
from libs import twitter
from libs.db import tweets_db


def generate_tweet(event, params):
    body = json.loads(event['body'])
    username = twitter.strip_username(body['username'])

    # Get tweets from twitter
    tweets = twitter.get_tweets(username)

    # Predict with GPT-3
    prediction = gpt.make_prediction(username, tweets)

    # Store on database
    tweet_id = tweets_db.insert_tweet({
        'tweet': prediction,
        'username': username,
        'views': 0
    })

    return {
        "tweetId": tweet_id,
        "tweet": prediction,
        "username": username
    }


def post(event, params):
    payload, status = handler.wrap_function(generate_tweet, event, params, 201)

    return {
        'statusCode': status,
        'headers': handler.get_headers('POST'),
        'body': json.dumps(payload)
    }
