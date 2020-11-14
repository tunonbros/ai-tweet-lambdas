import json
import os

# DON'T FORGET TO FILL ENVIRONMENT VARIABLES WHEN RELEASING

return_headers = {
    # CORS
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Origin': os.environ['DOMAIN'],
    'Access-Control-Allow-Methods': 'OPTIONS,GET',
    # Rest of headers
    'content-type': 'application/json'
}


def get(event, context):
    print(event)
    try:
        payload = {
            "username": "Juanito",
            "text": "This is so funny I had to share it"
        }
        status = 200
    except (ValueError, TypeError):
        payload = {"error": "Invalid format"}
        status = 400
    except Exception as e:
        print(f"ERROR - unknown exception: {type(e)} - {str(e)}")
        payload = {"error": "Unknown error"}
        status = 500

    return {
        'statusCode': status,
        'headers': return_headers,
        'body': json.dumps(payload)
    }
