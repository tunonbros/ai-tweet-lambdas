import generate_tweet
import shared
from libs import handler


proxy_mapping = {
    "ai-tweet-generate": {
        "POST": generate_tweet.post
    },
    "shared": {
        # "POST": shared.post,
        "GET": shared.get
    }
}


def not_found(event, context):
    return {
        'statusCode': 404,
        'headers': handler.get_headers(),
        'body': 'Not found'
    }


def entrypoint(event, context):
    method = event['requestContext']['http']['method']
    path_tokens = event['requestContext']['http']['path'].split("/")
    params = None
    if len(path_tokens) < 2:
        func = not_found
    else:
        func = proxy_mapping.get(path_tokens[1], {}).get(method, not_found)
        if len(path_tokens) > 2:
            params = path_tokens[2:]

    print(f"Function for path {path_tokens} and method {method}: {func.__name__}")
    return func(event, params)
