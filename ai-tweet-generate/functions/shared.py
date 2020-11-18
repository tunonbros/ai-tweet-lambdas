import json
from libs import handler
from libs.db import tweets_db


def post_shared(event):
    # tweets_db.insert_tweet({
    #     'tweet': 'You found a testing tweet. Easy, huh? Congratulations. There is no reward for it, though.',
    #     'username': 'betatester',
    #     'views': 0,
    #     'tweet_id': 'aaaaaaaaaa'
    # })
    pass


def get_shared(event):
    tweet_id = event['pathParameters']['tweetId']
    tweet = tweets_db.get_tweet(tweet_id)
    return dict(tweet.items())


def get(event, context):
    payload, status = handler.wrap_function(get_shared, event)

    return {
        'statusCode': status,
        'headers': handler.get_headers(),
        'body': json.dumps(payload, default=str)
    }
