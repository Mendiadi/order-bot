import os
from dataclasses import dataclass
from json_func import json_read, write_to_json
import requests

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


class Stock:
    def __init__(self, path: str):
        self.out_put_file = path
        self.stock = None
        self.products = []

    def load(self):
        if self.out_put_file in os.listdir():
            self.stock = json_read(self.out_put_file)
            self.products = [Product(**p) for p in self.stock["Stock"]]
        else:
            write_to_json({"Stock":[]},self.out_put_file,1)
            self.stock = json_read(self.out_put_file)

    def get_product(self, name):
        product = requests.get(f"http://127.0.0.1:5000/product/{name}")
        if product.ok:
            return Product(name=product.json()['name'],ammount=product.json()['amount'])
        return None

    def get_stock(self):
        res = requests.get("http://127.0.0.1:5000/product")
        for p in res.json():

            self.products.append(Product(name=p['name'],ammount=p['amount']))
        return {"Stock":res.json()}
    def get_stock_admin(self):
        res = requests.get("http://127.0.0.1:5000/product")

        for p in res.json():
            self.products.append(Product(name=p['name'], ammount=p['amount']))
        return {"Stock": res.json()}

    def add_product(self, pdt):
        requests.post("http://127.0.0.1:5000/product",json={"name":pdt.name,"amount":pdt.ammount})



    def remove_product(self, name) -> bool:
        res = requests.delete(f"http://127.0.0.1:5000/product/{name}")
        if res.ok:
            return True
        return  False
    def commit(self):
        self.stock["Stock"] = [p.save_ready() for p in self.products]
        write_to_json(self.stock, self.out_put_file, len(self.stock))
        print("[DB] commited.")
        print(f"[DB] {self.products}")


if __name__ == '__main__':
    a = Stock("data.json")
    a.load()
    a.products = [Product("shay",10),Product("adi",20)]
    a.commit()
    print(a.get_stock())