from groq import Groq
import os
import platform
import conf.config as cfg

api_key = cfg.api_key
system_content = cfg.system_content
model_type = cfg.assist_data["super_model"]["model_type"]["model_1"]

conversation_history = []


def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def process_model(msg_content):
    global conversation_history
    messages = conversation_history + [
        {"role": "user", "content": msg_content},
        {"role": "system", "content": system_content},
    ]
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model=model_type,
        messages=messages,
        temperature=0.1,
        max_tokens=3000,
        top_p=1,
        stream=True,
        stop="[transaction success and have been payed]",
    )
    return completion


def response_assistant(msg_content):
    completion = process_model(msg_content)
    response_text = "\nAssistant: \n"

    for chunk in completion:
        chunk_text = chunk.choices[0].delta.content or ""
        response_text += chunk_text

    else:
        print(response_text)

    conversation_history.append({"role": "assistant", "content": response_text})

    return response_text


def msg_data(msg_content):
    process_model(msg_content)
    response_assistant(msg_content)