from product_item import Stock


class Base_Menu:
    def __init__(self):
        self.state = "init"
        self.stock = Stock("./data_json.json")

    def get_stock(self):
        return self.stock.get_stock().encode("utf-8")

    def show(self):
        pass

    def heandler(self, message) -> str:
        pass
