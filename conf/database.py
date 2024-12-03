from supabase import create_client, Client
import os
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


# Insert data into recommendations table
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