import json
import gpt

return_headers = {
    # CORS
    'Access-Control-Allow-Headers': 'Content-Type',
    # 'Access-Control-Allow-Origin': 'http://www.ai-tweet.com',
    'Access-Control-Allow-Origin': 'http://localhost:3001',
    'Access-Control-Allow-Methods': 'OPTIONS,POST',
    # Rest of headers
    'content-type': 'application/json'
}


def lambda_handler(event, context):
    # print(event)
    try:
        body = json.loads(event['body'])
        prediction = gpt.make_prediction(body['username'])

        payload = {
            "text": prediction
        }
        status = 201
    except ValueError:
        payload = {"error": "Invalid format"}
        status = 400
    except Exception:
        payload = {"error": "Unknown error"}
        status = 500

    return {
        'statusCode': status,
        'headers': return_headers,
        'body': json.dumps(payload)
    }
