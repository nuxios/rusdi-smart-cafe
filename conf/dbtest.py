import json

with open('conf.json', 'r') as f:
    config = json.load(f)

url = config['SUPABASE_URL']
key = config['SUPABASE_KEY']

print(f"SUPABASE_KEY: {key}")
print(f"Key Length: {len(key)}")

from supabase import create_client, Client
supabase: Client = create_client(url, key)