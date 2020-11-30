import requests
import os
import json


def get_headers():
    return {"Authorization": f"Bearer {os.environ['TWITTER_BEARER_TOKEN']}"}


def get_timeline_url(username):
    return f'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={username}&count=5&trim_user=true'


def get_timeline(username):
    response = requests.request("GET", get_timeline_url(username), headers=get_headers())
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_tweets(username):
    timeline = [t['text'] for t in get_timeline(username)]
    print(json.dumps(timeline, indent=4))
    return timeline
