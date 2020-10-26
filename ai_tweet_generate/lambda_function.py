import json


def lambda_handler(event, context):
    print(event)

    payload = {
        "text": "Thanks for asking, but I'm not making predictions... yet..."
    }
    return {
        'statusCode': 201,
        'headers': {
            'content-type': 'application/json'
        },
        'body': json.dumps(payload)
    }
