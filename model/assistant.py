import re
from groq import Groq
import os
import platform
import psutil
import conf.config as cfg
import conf.database as db

api_key = cfg.api_key
system_content = cfg.system_content
model_type = cfg.assist_data["super_model"]["model_type"]["model_3"]

conversation_history = []
transcript_history = []

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
        temperature=0.3,
        max_tokens=8000,
        top_p=1,
        stream=True,
        stop="[transaction success and have been payed]",
    )
    return completion

def response_assistant(msg_content):
    global transcript_history
    completion = process_model(msg_content)
    response_text = "\nAssistant: \n"

    for chunk in completion:
        chunk_text = chunk.choices[0].delta.content or ""
        response_text += chunk_text

    if "TRANSCRIPT RUSDI SMART CAFE" in response_text:
        transcript_history.append(response_text)

        clear_terminal()

        print("=== TRANSCRIPT RUSDI SMART CAFE ===")
        dataitem = []
        
        for transcript in transcript_history:
            print(transcript)
            
            # Menangkap semua item_id, quantity, dan total_price
            item_id_match = re.findall(r"item_id:\s*([\w-]+)", transcript)
            quantity_match = re.findall(r"quantity:\s*(\d+)", transcript)
            total_price_match = re.findall(r"total_price:\s*Rp([\d,]+)", transcript)

            # Pastikan kita memiliki item_id, quantity, dan total_price yang sesuai
            if len(item_id_match) == len(quantity_match) == len(total_price_match):
                # Loop untuk setiap item yang ditemukan dalam transcript
                for i in range(len(item_id_match)):
                    item_id = item_id_match[i]
                    quantity = int(quantity_match[i])
                    total_price = float(total_price_match[i].replace(",", ""))

                    # Menambahkan item ke dalam dataitem
                    dataitem.append(
                        {
                            "item_id": item_id,
                            "quantity": quantity,
                            "total_price": total_price,
                        }
                    )

        # Menampilkan data yang berhasil diambil
        print(dataitem)

        if not dataitem:
            print("Gagal mendeteksi informasi transaksi. Tidak ada data yang valid.")
            return

        # Simpan transaksi ke database
        for item in dataitem:
            db.insert_transaction(item["item_id"], item["quantity"], item["total_price"])

        current_process = psutil.Process(os.getpid())
        current_process.terminate()
        print("Proses telah dihentikan!")

    else:
        print(response_text)

    conversation_history.append({"role": "assistant", "content": response_text})

    return response_text

def msg_data(msg_content):
    process_model(msg_content)
    response_assistant(msg_content)
