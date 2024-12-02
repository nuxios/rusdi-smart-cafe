def insert_data_dummy(data, insert_item):
    for item in data:
        insert_item(item["name"], item["category"], item["price"])
        

def update_data_dummy(data):
    pass