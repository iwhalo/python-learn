from openai import OpenAI
client=OpenAI()

resp=client.responses.create(
    model='gpt-5-nano',
    input="Write a one-sentence bedtime story about a unicorn."
)

print(resp.output_text)