import os
import openai

openai.api_key = os.getevn('OPENAI_KEY')


def generate_prompt(username):
    return f"""
Twitter is a platform where users share text messages up to 140 characters long.
These are some example tweets from an unknown user:
-> I'm so happy to see the sun rising up this morning #BeautifulMorning
-> I have mixed feelings about the ending of How I met your mother

The following are some examples of what {username} would post on Twitter:
->"""


def make_prediction(username):
    prompt = generate_prompt(username)
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
