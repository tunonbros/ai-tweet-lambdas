
import os
from .twitter import InvalidUsername, NoRecentTweets


def wrap_function(func, event, success_status=200):
    try:
        payload = func(event)
        status = success_status
    except (ValueError, TypeError):
        payload = {"error": "Invalid format"}
        status = 400
    except AttributeError:
        payload = {"error": "Not found"}
        status = 404
    except InvalidUsername as e:
        payload = {"error": str(e)}
        status = 404
    except NoRecentTweets as e:
        payload = {"error": str(e)}
        status = 204
    except Exception as e:
        print(f"ERROR - unknown exception: {type(e)} - {str(e)}")
        payload = {"error": "Unknown error"}
        status = 500
    return payload, status


def get_headers(method='GET'):
    # DON'T FORGET TO FILL ENVIRONMENT VARIABLES WHEN RELEASING

    return {
        # CORS
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Origin': os.environ['DOMAIN'],
        'Access-Control-Allow-Methods': f'OPTIONS,{method}',
        # Rest of headers
        'content-type': 'application/json'
    }


def to_camel_case(st):
    output = ''.join(x for x in st.replace('_', ' ').title() if x.isalnum())
    return output[0].lower() + output[1:]


def split_keys(data):
    for key, value in data:
        if isinstance(key, str):
            yield to_camel_case(key), key, value
        elif isinstance(key, dict):
            yield key.items()[0] + value
        else:
            raise Exception("Key not serializable")


def serialize(data, keys=None):
    if not keys:
        return dict(data)

    return {k_front: v for k_front, k_back, v in split_keys(data) if k_back in keys}
