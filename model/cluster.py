from groq import Groq
import json

with open("assist.json", "r") as assist_file:
    assist_data = json.load(assist_file)

with open("conf.json", "r") as config_file:
    config = json.load(config_file)

api_key = config["GROQ_KEY"]
assistant_content = assist_data["assistant"]["content"] 

def cluster_model(model_names, messages, temperature, max_tokens, top_p, stream, stop):
    pass

client = Groq(api_key=api_key)

completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {"role": "user", "content": "halo"},
        {"role": "system", "content": assistant_content},
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

# print(assistant_content)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
