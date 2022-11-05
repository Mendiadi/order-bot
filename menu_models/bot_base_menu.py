from bot_telegram.enums_schemas import Status
from bot_telegram.product_item import Stock


class MenuProtocol:
    actions: dict[str, str]

    def __init__(self):
        self.stock: Stock = Stock("./data_json.json")
        self.msg_stage: str = ""

    def get_stock(self):
        return self.stock.get_stock().encode("utf-8")


    def handle(self, bot, message,sender) -> str:

        if message not in self.actions:
            return Status.error
        return self.actions[message]
