from supabase import create_client, Client
import os
import sys
import json


# Function to connect to the database
def DB_connect():
    with open("conf.json", "r") as f:
        config = json.load(f)

    url = config["SUPABASE_URL"]
    key = config["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
    return supabase


# Insert data into items table
def insert_item(name, category, price):
    supabase = DB_connect()
    data = {
        "name": name,
        "category": category,
        "price": price,
    }
    response = supabase.table("items").insert(data).execute()
    print(response)


# Insert data into transactions table
def insert_transaction(item_id, quantity, total_price):
    supabase = DB_connect()
    data = {
        "item_id": item_id,
        "quantity": quantity,
        "total_price": total_price,
    }
    response = supabase.table("transactions").insert(data).execute()
    return response.data


def insert_recommendation(item_id):
    supabase = DB_connect()
    data = {
        "item_id": item_id,
    }
    response = supabase.table("recommendations").insert(data).execute()
    print(response)


def show_item():
    supabase = DB_connect()
    response = supabase.table("items").select("*").execute()

    return response.data

import datetime
from collections import defaultdict

def show_item():
    # Mendapatkan data dari tabel items
    supabase = DB_connect()
    response = supabase.table("items").select("*").execute()
    return response.data

def get_transactions():
    # Mendapatkan data transaksi dari tabel transactions
    supabase = DB_connect()
    response = supabase.table("transactions").select("*").execute()
    return response.data

# def generate_recommendations():
#     # Mendapatkan semua data item
#     items = show_item()
#     # Mendapatkan semua data transaksi
#     transactions = get_transactions()

#     # Dictionary untuk menyimpan penjualan berdasarkan item_id per hari
#     sales_count = defaultdict(lambda: defaultdict(int))  # Struktur: {day_of_week: {item_id: count}}

#     # Menghitung jumlah penjualan berdasarkan hari dalam seminggu
#     for transaction in transactions:
#         # Mendapatkan timestamp penjualan
#         timestamp = transaction['transaction_date']  # Asumsikan 'created_at' menyimpan waktu penjualan
#         day_of_week = datetime.time(timestamp, "%Y-%m-%dT%H:%M:%S.%f").weekday()

#         # Mengupdate jumlah penjualan berdasarkan item_id dan hari dalam seminggu
#         item_id = transaction['item_id']
#         quantity = transaction['quantity']
#         sales_count[day_of_week][item_id] += quantity

#     # Menyusun rekomendasi berdasarkan penjualan tertinggi untuk setiap hari dalam seminggu
#     recommendations = []
#     for day, items_sales in sales_count.items():
#         # Mengurutkan item berdasarkan jumlah penjualan, tertinggi ke terendah
#         sorted_items = sorted(items_sales.items(), key=lambda x: x[1], reverse=True)
#         if sorted_items:
#             # Ambil item dengan penjualan tertinggi
#             top_item_id = sorted_items[0][0]
#             recommendations.append({
#                 "item_id": top_item_id,
#                 "day_available": [day]
#             })

#     # Insert rekomendasi ke tabel recommendations
#     supabase = DB_connect()
#     for recommendation in recommendations:
#         supabase.table("recommendations").insert(recommendation).execute()

#     print("Rekomendasi berhasil dibuat dan dimasukkan ke dalam tabel recommendations.")

# # Menjalankan fungsi generate_recommendations untuk membuat rekomendasi harian
# generate_recommendations()


def recommendations_get_all():
    supabase = DB_connect()
    response = supabase.table("recommendations").select("*").execute()
    return response.data


def recommendations_day():
    day_of_week = datetime.datetime.now().weekday()
    data = recommendations_get_all()

    if not data:
        print("Tidak ada data rekomendasi tersedia.")
        return []
    daily_recommendations = []

    for item in data:
        if "day_available" in item and day_of_week in item["day_available"]:
            daily_recommendations.append(item)

    if not daily_recommendations:
        print("Tidak ada rekomendasi menu untuk hari ini.")
        return []

    return daily_recommendations


# recommendations_today = recommendations_day()
# if recommendations_today:
#     for rec in recommendations_today:
#         print(f"Rekomendasi untuk hari ini: {rec['item_name']} - {rec['description']}")