import sys
import os
import re
import conf.database as db

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

conversation_history = []


def menu_cafe():

    menu = db.show_item()
    return menu


def assistant(msg_content):
    import json
    from groq import Groq

    with open("assist.json", "r") as assist_file:
        assist_data = json.load(assist_file)

    with open("conf.json", "r") as config_file:
        config = json.load(config_file)

    api_key = config["GROQ_KEY"]
    assistant_content = assist_data["assistant"]["content"]

    menu_items = menu_cafe()
    menu_text = "\n".join(
        [
            f"- {item['id']} - {item['name']} ({item['category']}): Rp{item['price']}"
            for item in menu_items
        ]
    )

    system_content = (
        assistant_content
        + " Ini adalah menu dari Rusdi Smart Cafe:\n"
        + str(menu_text)
        + "\n\n"
        + " Harus menggunakan bahasa indonesia jaksel "
        + "Jangan menyebutkan langsung data menu dalam bentuk daftar. "
        + "Sebaliknya, sajikan menu dengan cara yang menarik dan tetap menjaga akurasi data dari array menu yang diberikan."
        + " Jika ada pertanyaan tentang menu, jawab dengan mengacu pada data menu yang diberikan."
        + " Jika ada pertanyaan yang tidak terkait dengan menu, jawab dengan cara yang ramah dan sesuai dengan peranmu sebagai asisten."
        + " Jangan jawab hal lain apalagi kata kata kasar dan tidak senonoh."
        + " tolong juga agar SOP yang diberikan di atas dijaga."
        + " seperti ini :"
        + " 1. Mengucapkan selamat datang"
        + " 2. Memberikan menu rekomendasi sesuai kategori"
        + " 3. Menjawab pertanyaan tentang menu dengan mengacu pada data menu yang diberikan."
        + " 4. Menjawab pertanyaan yang tidak terkait dengan menu dengan cara yang ramah dan sesuai dengan peranmu sebagai asisten."
        + " 5. Jangan jawab hal lain apalagi kata kata kasar dan tidak senonoh."
        + " 6. Jangan menyebutkan langsung data menu dalam bentuk daftar."
        + " 7. Sajikan menu dengan cara yang menarik dan tetap menjaga akurasi data dari array menu yang diberikan."
        + " 8. Sebelum membuat transcript tawarkan terlebih dahulu makanan rekomendasi atau ketika si pembeli tidak mau makanan atau minuman yang lainnya baru di kasih transcript ketika ia telah membayar makanan"
        + " 9. Jika ada pertanyaan tentang pembayaran, jawab dengan memberikan informasi tentang metode pembayaran yang tersedia."
        + " 10. Jika ada pertanyaan tentang lokasi, jawab dengan memberikan informasi tentang lokasi Rusdi Smart Cafe."
        + " 11. Jika ada pertanyaan tentang jam buka, jawab dengan memberikan informasi tentang jam buka Rusdi Smart Cafe."
        + " 12. Jika ada pertanyaan tentang kontak, jawab dengan memberikan informasi tentang kontak Rusdi Smart Cafe."
        + " tolong untuk transcript di buat dan di perbolehkan hanya ketika dia sudah tidak ingin apa apa lagi, dan ketika dia bertanya pesanan dia apa saja jangan langsung menunjukan transcript nya tapi dia hanya menunjukkan nama dari pesanan dia dan harga nya sekaligus quantity nya saja oke? dan agar harus mempunyai item_id, quantity, dan total_price. dan juga data nya di pisah ya sesuai sama item_id dari item tersebut. jadi semisal kalau beli croissant 3x dan juga espresso 1x nah berarti kita bikin 2 data transcript yang berbeda. dan juga total_price nya harus di hitung dari quantity nya ya. nah baru setelah itu bikin transcript kedua untuk espresso dan lakukan hal yang sama. tolong dibuat seperti ini: "
        + """
        untuk transcript kamu harus buat seperti table persis:
        
        =====================================================================
        TRANSCRIPT
        =====================================================================
        |  Name  |Quantity | Price  | category |\
        |--------|---------|--------|----------|
        |Spagethi| 1       |15.000  | Beverage |\
        |        |         |        |          |\
        |        |         |        |          |\
        =====================================================================
        pesanan: 1 croissant (3x) dan 1 espresso (1x) (contoh)
        item_id: (isi id item saja)
        quantity: 1
        total_price: Rp35000
       
        """
        + " tolong untuk tidak asal mengirim transcript kecuali si user sudah di pastikan membayar"
    )

    global conversation_history
    messages = conversation_history + [
        {"role": "user", "content": "\n" + msg_content},
        {"role": "system", "content": system_content},
    ]

    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=messages,
        temperature=0.2,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    response_text = "\nAssistant: "
    for chunk in completion:
        chunk_text = chunk.choices[0].delta.content or ""
        response_text += chunk_text

    print(response_text)

    if (
        "transcript" in response_text.lower()
        and "quantity:" in response_text.lower()
        and "item_id" in response_text.lower()
        and "total_price" in response_text.lower()
    ):
        handle_transcript(response_text)

    conversation_history.append({"role": "assistant", "content": response_text})
    return response_text


def handle_transcript(response_text):

    try:
        transcripts = response_text.split("Transcript")

        dataitem = []

        for transcript in transcripts:
            if (
                "item_id" in transcript
                and "quantity" in transcript
                and "total_price" in transcript
            ):
                item_id_match = re.search(r"item_id:\s*([\w-]+)", transcript)
                quantity_match = re.search(r"quantity:\s*(\d+)", transcript)
                total_price_match = re.search(r"total_price:\s*Rp([\d,]+)", transcript)

                if item_id_match and quantity_match and total_price_match:
                    item_id = item_id_match.group(1)
                    quantity = int(quantity_match.group(1))
                    total_price = float(total_price_match.group(1).replace(",", ""))

                    dataitem.append(
                        {
                            "item_id": item_id,
                            "quantity": quantity,
                            "total_price": total_price,
                        }
                    )
                    print(dataitem)
        if not dataitem:
            # print("Gagal mendeteksi informasi transaksi. Tidak ada data yang valid.")
            return

        for item in dataitem:
            db.insert_transaction(
                item["item_id"], item["quantity"], item["total_price"]
            )
        # print("Transaksi berhasil disimpan ke Supabase.")

    except Exception as e:
        # print(f"Error menyimpan transaksi: {e}")
        pass
