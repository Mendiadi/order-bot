import json
from dataclasses import dataclass
from json_func import json_read, write_to_json


@dataclass
class UserInfo:
    user_id: int
    user_name: str


@dataclass
class Product():
    name: str
    ammount: int

    def __str__(self):
        return f"מוצר: {self.name} " \
               f"\n" \
               f"    כמות: {self.ammount} \n"

    def save_ready(self):
        return {
            "name": self.name,
            "ammount": self.ammount
        }


class Stock():
    def __init__(self, path: str):
        self.out_put_file = path
        self.stock = None
        self.products = None

    def load(self):
        self.stock = json_read(self.out_put_file)
        self.products = [Product(**p) for p in self.stock["Stock"]]

    def get_product(self, name):
        for item in self.products:
            if item.name == name:
                return item
        return None

    def get_stock(self):
        tmp_stock = ""
        for index, value in enumerate(self.products):
            tmp_stock += f"{index + 1}) {value.name} \n"
        return tmp_stock

    def get_stock_admin(self):
        tmp_stock = "מצב מלאי :\n"
        for index, value in enumerate(self.products):
            tmp_stock += f"{index + 1}) {value}"
        tmp_stock += f"."
        return tmp_stock

    def add_product(self, pdt):
        self.products.append(pdt)

    def remove_product(self, name) -> bool:
        item = self.get_product(name)
        if item:
            self.products.remove(item)
            self.commit()
            return True
        else:
            return False

    def commit(self):
        self.stock["Stock"] = [p.save_ready() for p in self.products]
        write_to_json(self.stock, 'data_json.json', len(self.stock))
        print("[DB] commited.")
        print(f"[DB] {self.products}")
