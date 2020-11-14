import json
from libs import gpt
from libs import handler


def generate_tweet(event):
    body = json.loads(event['body'])
    prediction = gpt.make_prediction(body['username'])
    return {
        "text": prediction
    }


def post(event, context):
    payload, status = handler.wrap_function(generate_tweet, event, 201)

    return {
        'statusCode': status,
        'headers': handler.get_headers('POST'),
        'body': json.dumps(payload)
    }
