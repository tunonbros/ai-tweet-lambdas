import os
import openai

openai.api_key = os.environ['OPENAI_KEY']


def generate_prompt(username, tweets):
    s = f"""
Twitter is a platform where users share text messages up to 140 characters long.

The following are some examples of what {username} uses to post on Twitter:
-> """
    tweets_str = "\n-> ".join(tweets)
    return s + tweets_str + "\n->"


def make_prediction(username, tweets):
    prompt = generate_prompt(username, tweets)
    print(prompt)
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=80, stop='->')
    print(response)

    # Example response
    # {
    #   "id": "cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7",
    #   "object": "text_completion",
    #   "created": 1589478378,
    #   "model": "davinci:2020-05-03",
    #   "choices": [
    #     {
    #       "text": " there was a girl who",
    #       "index": 0,
    #       "logprobs": null,
    #       "finish_reason": "length"
    #     }
    #   ]
    # }
    return str(response['choices'][0]['text'])
