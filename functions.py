from dataclasses import dataclass
import json

@dataclass
class Product():
    name: str
    ammount : int

    def __str__(self):
        return fr"\nשם המוצר:{self.name} \n כמות:{self.ammount}\n"



def get_stock():
    """
    preparing data for the tests2 from json file.
    :return: json : data for tests2.
    """
    with open('data_json.json') as file_root:
        file_json_data = json.load(file_root)
    return file_json_data

# def edit_inventory(name,ammount):
#     data = get_stock()
#     for item in data['Stock']:
#         if item["name"] == name:
#             item["ammount"] = ammount
#     with open('data_json.json', 'w') as f:
#         json.dump(data, f)

# def add_to_inventory(item):
#     edit_inventory(item)

def get_inventory():
    stock_lst = []
    for item in get_stock()["Stock"]:
        temp_item = Product(**item)
        stock_lst.append(temp_item)
    return stock_lst

def make_order(bot,message):
    cart = ""
    flag = True
    bot.reply_to(message,get_inventory())
    while flag:
        item = input("אנא בחר מוצר להוסיף לעגלה")
        bot.reply_to(message,)
    print("")

