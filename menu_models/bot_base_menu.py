from enums_schemas import Status
from product_item import Stock


class MenuProtocol:
    actions: dict[str, str]

    def __init__(self,stock:Stock):
        self.stock: Stock = stock
        self.msg_stage: str = ""


    def handle(self, bot, message,sender) -> str:

        if message not in self.actions:
            return Status.error
        return self.actions[message]
