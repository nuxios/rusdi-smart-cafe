import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import conf.database as db

# Temporary memory untuk menyimpan percakapan
conversation_history = []

def menu_cafe():
    # Ambil menu dari database
    menu = db.show_item()
    return menu

def assistant(msg_content):
    import json
    from groq import Groq

    # Load file assist.json dan conf.json
    with open("assist.json", "r") as assist_file:
        assist_data = json.load(assist_file)

    with open("conf.json", "r") as config_file:
        config = json.load(config_file)

    api_key = config["GROQ_KEY"]
    assistant_content = assist_data["assistant"]["content"]

    # Ambil data menu dari cafe
    menu_items = menu_cafe()

    # Konversi menu menjadi teks
    menu_text = "\n".join(
        [
            f"- {item['name']} ({item['category']}): Rp{item['price']}"
            for item in menu_items
        ]
    )

    # Gabungkan data assistant_content dengan menu cafe
    system_content = (
        assistant_content
        + " Ini adalah menu dari Rusdi Smart Cafe:\n"
        + str(menu_text)
        + "\n\n"
        + "Jangan menyebutkan langsung data menu dalam bentuk daftar. "
        + "Sebaliknya, sajikan menu dengan cara yang menarik dan tetap menjaga akurasi data dari array menu yang diberikan."
    )

    # Tambahkan riwayat percakapan ke dalam pesan
    global conversation_history
    messages = conversation_history + [
        {"role": "user", "content": msg_content},
        {"role": "system", "content": system_content},
    ]

    # Inisialisasi Groq client
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.2,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Ambil respon dari AI dan tambahkan ke riwayat percakapan
    response_text = ""
    for chunk in completion:
        chunk_text = chunk.choices[0].delta.content or ""
        print(chunk_text, end="")
        response_text += chunk_text

    # Simpan balasan AI ke dalam riwayat
    conversation_history.append({"role": "assistant", "content": response_text})