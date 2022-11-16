import json
import os
from dataclasses import dataclass
from json_func import json_read, write_to_json
import requests


@dataclass
class Product():
    name: str
    ammount: int

    def __str__(self):
        return f"""מוצר: {self.name}    כמות:{self.ammount}
        """

    def __repr__(self):
        return str(self)

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
        ...

    def get_product(self, name):
        product = requests.get(f"http://127.0.0.1:5000/product/{name}")
        if product.ok:
            return Product(name=product.json()['name'], ammount=product.json()['amount'])
        return None

    def get_stock(self):
        res = requests.get("http://127.0.0.1:5000/product")
        for p in res.json():
            self.products.append(Product(name=p['name'], ammount=p['amount']))
        return [str(i.name) for i in self.products]

    def get_stock_admin(self):
        res = requests.get("http://127.0.0.1:5000/product")
        for p in res.json():
            self.products.append(Product(name=p['name'], ammount=p['amount']))
        return [str(i) for i in self.products]

    def add_product(self, pdt):
        requests.post("http://127.0.0.1:5000/product", json={"name": pdt.name, "amount": pdt.ammount})

    def update(self, pdt):
        requests.put(f"http://127.0.0.1:5000/product/{pdt.name}", json={"name": pdt.name, "amount": pdt.ammount})

    def remove_product(self, name) -> bool:
        res = requests.delete(f"http://127.0.0.1:5000/product/{name}")
        if res.ok:
            return True
        return False

    def commit(self):
        ...


if __name__ == '__main__':
    a = Stock("data.json")
    a.load()
    a.products = [Product("shay", 10), Product("adi", 20)]
    a.commit()
    print(a.get_stock())
