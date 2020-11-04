import openai

openai.api_key = "not-a-real-api-key"


def generate_prompt(username):
    return f"Twitter is a platform where users share text messages up to 140 characters long. If {username} was alive he/she would probably tweet:\n-"


def make_prediction(username):
    prompt = generate_prompt(username)
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=60, stop='-')
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
