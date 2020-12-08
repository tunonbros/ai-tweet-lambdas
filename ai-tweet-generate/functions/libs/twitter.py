import requests
import json
import os
import re


class InvalidUsername(Exception):
    pass


class NoRecentTweets(Exception):
    pass


def get_headers():
    return {"Authorization": f"Bearer {os.environ['TWITTER_BEARER_TOKEN']}"}


def get_timeline_url(username, limit):
    return f'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={username}&count={limit}&trim_user=true&include_rts=false'


def get_timeline(username, limit=5):
    response = requests.request("GET", get_timeline_url(username, limit), headers=get_headers())
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise InvalidUsername("User not found in twitter")
    else:
        raise Exception(response.status_code, response.text)


def get_tweets(username):
    limits = [5, 15]
    for lim in limits:
        timeline = [t['text'] for t in get_timeline(username, lim)]
        if timeline:
            print(json.dumps(timeline, indent=4))
            return timeline
    raise NoRecentTweets("The user does not have any recent original content")


def strip_username(username):
    pattern = re.compile('[^A-Za-z0-9_]+', re.UNICODE)
    stripped_username = pattern.sub('', username)
    if len(stripped_username) > 15 or len(stripped_username) < 4:
        raise InvalidUsername("Invalid username")
    return stripped_username
