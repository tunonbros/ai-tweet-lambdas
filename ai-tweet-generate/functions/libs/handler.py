
import os


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
