import json
from dataclasses import dataclass
from json_func import json_read, write_to_json
from product_item import Product

class Order_Status:
    pending = "pending"
    canceled = "canceled"
    approved = "approved"


@dataclass
class OrderObj():
    cart: {}
    phone: str
    address: str
    order_state: Order_Status

    # def __str__(self):
    #     return f"user_id {self.user_id}\n \
    #             talk_status {self.talk_status}\n \
    #             nemu_state {self.menu_state}"

    def save_ready(self):
        return {
            "cart": {self.cart['p'],self.cart['amount']},
            "phone": self.phone,
            "address": self.address,
            "order_state": self.order_state
        }


@dataclass
class ActiveTalk():
    user_id: str
    talk_status: None
    menu_state: None

    def __str__(self):
        return f"user_id {self.user_id}\n \
                talk_status {self.talk_status}\n \
                nemu_state {self.menu_state}"

    def save_ready(self):
        return {
            "user_id": self.user_id,
            "talk_status": self.talk_status,
            "nemu_state": self.menu_state
        }


class OrdersMeneger():

    def __init__(self, path: str):
        self.out_put_file = path
        self.orders_stock = None
        self.orders = []

    def load(self):
        self.orders_stock = json_read(self.out_put_file)
        self.orders = [OrderObj(**p) for p in self.orders_stock["Orders"]]

    def get_orders(self):
        tmp_stock = ""
        for index,value in enumerate(self.orders):
            tmp_stock += f"{index+1}) {value} \n"
        return tmp_stock

    def add_order(self, order):
        self.orders.append(order)

    def commit(self):
        self.orders_stock["Orders"] = [p.save_ready() for p in self.orders]
        write_to_json(self.orders_stock, self.out_put_file, len(self.orders_stock))
        print("[DB] commited.")
        print(f"[DB] {self.orders}")
