import json
import conf.database as db
from datetime import datetime
import pytz


def menu_cafe():
    menu = db.show_item()
    return menu

def raw_material():
    raw_materials = db.show_raw_materials()
    return raw_materials


utc_now = datetime.now(pytz.utc)

# Mengonversi waktu UTC ke Asia/Jakarta
jakarta_tz = pytz.timezone("Asia/Jakarta")
jakarta_now = utc_now.astimezone(jakarta_tz)

menu_items = menu_cafe()
menu_text = "\n".join(
    [
        f"- id:{item['id']} - {item['name']} - ({item['category']}): Rp{item['price']}"
        for item in menu_items
    ]
)

rawmat_item = raw_material()
rawmat_text  = "\n".join(
    [
        f"- id:{item['id']} - name: {item['name']} - stock: {item['stock']} - unit: {item['unit']}"
        for item in rawmat_item
    ]
)

with open("assist.json", "r") as assist_file:
    assist_data = json.load(assist_file)

with open("conf.json", "r") as config_file:
    config = json.load(config_file)


api_key = config["GROQ_KEY"]
assistant_content = assist_data["system"]["content"]

custom_model = "Data diri (identitas) kamu:" "\nNama kamu adalah: " + assist_data[
    "super_model"
]["name_model"] + "\nBahasa yang kamu gunakan adalah " + assist_data["super_model"][
    "language_model"
] + "\nNama Owner kamu adalah " + assist_data[
    "super_model"
][
    "owner_info"
][
    "name_owner"
] + "\nContact owner : " + assist_data[
    "super_model"
][
    "owner_info"
][
    "contact"
] + "\n Timezone kamu adalah Asia/Jakarta: " + jakarta_now.strftime(
    "%Y-%m-%d %H:%M:%S"
)


system_content = (
    assistant_content
    + custom_model
    + """
    
Assistant Rules:
1. Jika ada bahan baku yang stoknya hampir habis, tampilkan daftar bahan baku dengan stok rendah.
2. Berikan rekomendasi pembelian bahan baku berdasarkan kebutuhan setiap menu.
3. Jangan memberikan informasi yang tidak relevan dengan bahan baku atau stok.
4. Analisis harus akurat dan membantu pemilik untuk melakukan pembelian bahan baku yang diperlukan.
5. Sertakan satuan bahan baku (contoh: gram, liter, pcs) dalam laporan.
6. Jika semua stok bahan baku cukup, beri tahu bahwa stok saat ini mencukupi.
7. Semua laporan harus dalam bentuk teks sederhana tanpa markdown atau simbol khusus.
8. Jika ada bahan baku yang stoknya habis, beri tahu pemilik untuk segera membeli bahan baku tersebut.
9. Jika ada bahan baku yang stoknya habis, jangan sertakan bahan baku tersebut dalam rekomendasi pembelian bahan baku.





  
"""
    + """
SOP Analisis Bahan Baku:
1. Tampilkan bahan baku yang stoknya hampir habis (di bawah ambang batas 50 unit).
2. Berikan rekomendasi bahan baku berdasarkan kebutuhan per menu.
3. Jika semua stok bahan baku cukup, beri tahu bahwa stok saat ini mencukupi.
4. Semua laporan harus dalam bentuk teks sederhana tanpa markdown atau simbol khusus.
5. Jika semua bahan baku yang di butuhkan siap buat di analisis maka kamu akan otomatis prediksi harga bahan baku sesuai takarannya untuk setiap stock yang di butuhkan sehingga nanti nya ketika sudah meminta transcript maka otomatis akan di jumlah dan di total
6. kamu tidak boleh memberikan tenggat waktu kecuali kamu memberikan transcript.
7. Tolong agar meminta konfirmasi terlebih dahulu sebelum membuat transcript/nota laporan bahan baku nya.
8. Jika belum meminta nota/transcript laporan bahan baku maka kamu jangan membuat nya.
9. Ingat kamu ini bukan melakukan transaksi tapi hanya mengirimkan laporan saja.
10. Kamu harus mengisi tenggat waktu nya dengan cara analisa kira kira berapa maximal waktu untuk mengirimkan laporan ke supplier agar di restock lagi bahan baku nya sebelum bahan bahan nya habis


"""    
    + """Ini dia stock bahan baku nya:  


"""
    + str(rawmat_text)
    + """
    
    
    
    
    
ini adalah menu nya: 
"""
    + str(menu_text)
    + """
ini adalah contoh nota laporan nya:


====================================================================
              LAPORAN STOK BAHAN BAKU NOTA PEMBELIAN                        
====================================================================
Nama Bahan       : Tepung Terigu  
Kebutuhan        : 50 gram  
Stok Saat Ini    : 30 gram  
Harga Per Satuan : Rp 20.000  
Keterangan       : Tambahkan 20 gram  

Nama Bahan       : Mentega  
Kebutuhan        : 10 gram  
Stok Saat Ini    : 20 gram  
Harga Per Satuan : Rp 10.000  
Keterangan       : Stok mencukupi  

====================================================================
Menu Terkait:  
- Croissant (membutuhkan 25 gram Tepung Terigu).  
- Cinnamon Roll (membutuhkan 20 gram Tepung Terigu).  

====================================================================
Estimasi Total Biaya:  
- Tepung Terigu: Rp 8.000 (40% dari Rp 20.000).  

Tenggat Waktu Pembelian: 17 Januari 2025  
====================================================================






[transaction success and have been payed]
"""
)