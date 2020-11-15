import json
from libs import handler


def get_shared(event):
    tweet_id = event['pathParameters']['tweetId']
    return {
        "username": f"Juanito: {tweet_id}",
        "text": "This is so funny I had to share it"
    }


def get(event, context):
    payload, status = handler.wrap_function(get_shared, event)

    return {
        'statusCode': status,
        'headers': handler.get_headers(),
        'body': json.dumps(payload)
    }
